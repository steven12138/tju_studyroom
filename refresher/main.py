import argparse
import os
import sys
import time
import traceback
from datetime import datetime, timedelta

import schedule
from tqdm import tqdm

from utils.util import print_flush
from utils.database_operations import sync_campus, sync_buildings, sync_rooms, sync_status, check_connection, \
    delete_previous_record
from utils.login import LoginLoader
from utils.status_fetcher import StatusFetcher
import re

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'

usr = os.getenv("CLASSES_USER")
pwd = os.getenv("CLASSES_PASSWORD")
assert usr is not None and pwd is not None, f"{RED}Please set CLASSES_USER and CLASSES_PASSWORD in environment variables{RESET}"

# Check Proxy
if os.getenv("HTTP_PROXY") is not None or os.getenv("HTTPS_PROXY") is not None:
    print_flush(f"{YELLOW}==> Using Proxy for HTTP:{os.getenv('HTTP_PROXY')}{RESET}")
    print_flush(f"{YELLOW}==> Using Proxy for HTTPS:{os.getenv('HTTPS_PROXY')}{RESET}")
    print_flush(f"{YELLOW}==> Wait 10s For EasyConnect-Docker To Start{RESET}")
    time.sleep(10)

cooldown_time = float(os.getenv("COOLDOWN_TIME", 0.7))
fetch_delta = int(os.getenv("FETCH_DELTA", 7))
run_at = os.getenv("RUN_AT", "01:00")
assert re.match(r"^\d{2}:\d{2}(:\d{2})?$", run_at) is not None, f"{RED}RUN_AT should be in format HH:MM(:SS){RESET}"

# Urgent Mail Notification
smtp_server = os.getenv("STMP_SERVER")
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASSWORD")
smtp_admin = os.getenv("ADMIN_MAIL")
smtp_port = os.getenv("SMTP_PORT")
should_mail_notify = smtp_server is not None and smtp_pass is not None and smtp_user is not None

# Print Config
print_flush("==> Starting Refresher")
print_flush("-------------------------------------------")
print_flush("     Forward Days:        ", f"{fetch_delta} days")
print_flush("     Cooldown Time:       ", f"{cooldown_time}s")
print_flush("     Username:            ", usr)
print_flush("     Run At:              ", run_at)
print_flush()
print_flush("     SQL Host:            ", os.getenv("SQL_URL", "localhost"))
print_flush("     SQL Port:            ", os.getenv("SQL_PORT", "3306"))
print_flush("     SQL User:            ", os.getenv("SQL_USER", "studyroom"))
print_flush("     SQL Database:        ", os.getenv("DATABASE", 'studyroom'))
print_flush()
print_flush("     Smtp Server:         ", smtp_server)
print_flush("     Smtp Port:           ", smtp_port)
print_flush("     Smtp User:           ", smtp_user)
print_flush("     Admin Email:         ", smtp_admin)
print_flush("-------------------------------------------")
print_flush("==> Trying to Login")
login_loader = LoginLoader(usr, pwd)
x = login_loader.login()
print_flush("==> Login Success, Starting Fetcher")

status_fetcher = StatusFetcher(session=x, wait_time=cooldown_time)


def refresh_login_status() -> None:
    global login_loader, x, status_fetcher
    print_flush("==> Refreshing Login Session")
    login_loader = LoginLoader(usr, pwd)
    x = login_loader.login()
    status_fetcher = StatusFetcher(session=x, wait_time=cooldown_time)
    print_flush("==> Login Session Updated")


def refresh(retry=3) -> dict[datetime, list]:
    refresh_login_status()
    now = datetime.now()
    result = {}
    date_bar = tqdm(range(0, fetch_delta), unit="day")
    for shift in date_bar:
        date = now + timedelta(days=shift)
        date_formatted = date.strftime("%Y-%m-%d")
        date_bar.set_description(f'Fetching data for date: {date_formatted}')
        for times in range(retry):
            try:
                raw_data = status_fetcher.fetch_date(date)
                result[date] = raw_data
                break
            except BaseException as e:
                if times == retry - 1:
                    print_flush(f"{RED}Reached Maximum Retries, Task Failed{RESET}")
                    raise

                print_flush()
                print_flush(f"{RED}Error when fetching data for date: ", date, f"retrying:{times + 1}/3", f"{RESET}")
                print_flush(f"{RED}Exceptions Detail: ", e, f"{RESET}")
                traceback.print_exc()
                time.sleep(2)
                refresh_login_status()
    return result


def unique_buildings(result: dict[datetime, list]) -> list[dict[str, str]]:
    buildings = []
    building_info: list[dict[str, str]] = []
    for date, data in result.items():
        for status in data:
            for item in status:
                # print_flush(item)
                if item["building"] not in buildings:
                    buildings.append(item["building"])
                    building_info.append({
                        'name': item['building'],
                        'campus': item['campus'],
                    })
    return building_info


def unique_campus(result: dict[datetime, list]) -> list[str]:
    campus = []
    for date, data in result.items():
        for status in data:
            for item in status:
                if item["campus"] not in campus:
                    campus.append(item["campus"])
    return campus


def unique_room(result: dict[datetime, list]) -> list[dict[str, str]]:
    room = []
    room_info: list[dict[str, str]] = []
    for date, data in result.items():
        for status in data:
            for item in status:
                if item["room"] not in room:
                    room.append(item["room"])
                    room_info.append({
                        'name': item['room'],
                        'building': item['building'],
                    })
    return room_info


def update_basic_info(
        campus: list[str],
        buildings: list[dict[str, str]],
        rooms: list[dict[str, str]]
) -> None:
    try:
        print_flush("==> Syncing Campus Info")
        sync_campus(campus)

        print_flush("==> Syncing Building Info")
        sync_buildings(buildings)

        print_flush("==> Syncing Room Info")
        sync_rooms(rooms)
    except Exception as e:
        print_flush("==> Syncing Failed With Error:")
        print_flush(e)
        raise


def mail_admin():
    pass


def retry_decorator(max_retries=3, delay_seconds=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print_flush()
                    print_flush(f"{RED}==> Exception Occurred: ", e, f"{RESET}")
                    traceback.print_exc()
                    retries += 1
                    print_flush(
                        f"{YELLOW}==> Retry: {retries}/{max_retries}, Waiting {delay_seconds} s for retry{RESET}")
                    time.sleep(delay_seconds)
                    refresh_login_status()

            print_flush(f"{RED}Reached Maximum Retries, Task Failed{RESET}")
            if should_mail_notify:
                mail_admin()

        return wrapper

    return decorator


@retry_decorator()
def task() -> None:
    # logs
    print_flush("--------------------")
    print_flush("==> Starting Task")
    print_flush("==> Current Date: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # database connection check
    print_flush("==> Checking Database Connection")
    print_flush("Result.......    ", end='')
    check_connection()
    print_flush(f"{GREEN}[PASSED]{RESET}")

    # refresh classroom info
    final_result = refresh()

    # refresh campus info
    campus = unique_campus(final_result)
    buildings = unique_buildings(final_result)
    rooms = unique_room(final_result)
    update_basic_info(campus, buildings, rooms)
    delete_previous_record(datetime.now())

    # sync status
    sync_status(final_result)

    print_flush("==> Task Finished")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--immediate', '-I', action='store_true', help="fetch data immediately and exit")
    args = parser.parse_args()

    if args.immediate:
        print_flush("==> Run Task Immediately")
        task()
        exit(0)

    print_flush("==> Starting Scheduler")
    print_flush("==> Task Will Run At 02:00 Every Day")
    print_flush("==> Checking Database Connection")
    print_flush("Result.......    ", end='')
    check_connection()
    print_flush(f"{GREEN}[PASSED]{RESET}")
    print_flush(flush=True)
    schedule.every().day.at(run_at).do(task)

    if os.getenv("IMMEDIATE") is not None:
        print_flush("==> Run Task Immediately")
        task()

    print_flush("==> Scheduler Started")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
