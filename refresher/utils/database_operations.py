import os
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .sql_entity import Base, Campus, Building, Room, Status
from .util import *

database_name = os.getenv("DATABASE", 'studyroom')
database_user = os.getenv("SQL_USER", 'studyroom')
database_password = os.getenv("SQL_PASS", '123456')
database_url = os.getenv("SQL_URL", 'localhost')
database_port = os.getenv("SQL_PORT", '3306')

engine = create_engine(
    f'mysql+pymysql://{database_user}:{database_password}@{database_url}:{database_port}/{database_name}')

Session = sessionmaker(bind=engine)


def check_connection() -> None:
    global Session, engine
    last_error = None
    for i in range(3):
        try:
            session = Session()
            session.execute(text('SELECT 1'))
            session.close()
            return
        except Exception as e:
            last_error = e
            print_flush(f"{RED}==> Connection Error{RESET}")
            print_flush(e)
            print_flush("==> Refresh Connection Session, retrying:", i + 1, "/3")
            engine = create_engine(
                f'mysql+pymysql://{database_user}:{database_password}@{database_url}:{database_port}/{database_name}')
            Session = sessionmaker(bind=engine)

    print_flush("==> Failed to connect to database")
    raise last_error


def ensure_schema() -> None:
    Base.metadata.create_all(engine)


def sync_campus(campuses: list[str]):
    session = Session()
    try:
        existing_campuses = set(session.query(Campus.name).all())
        new_campuses = [Campus(name=name) for name in campuses if (name,) not in existing_campuses]

        if new_campuses:
            session.add_all(new_campuses)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def sync_buildings(buildings: list[dict[str, str]]) -> None:
    session = Session()
    try:
        existing_buildings = {
            (building.campus_id, building.name)
            for building in session.query(Building).all()
        }
        campus_ids = {campus.name: campus.id for campus in session.query(Campus).all()}

        buildings_to_add = []
        for building in buildings:
            campus_id = campus_ids.get(building['campus'])
            if campus_id is None:
                raise ValueError("Unexpected campus name: " + building['campus'])

            building_key = (campus_id, building['name'])
            if building_key in existing_buildings:
                continue

            buildings_to_add.append(Building(name=building['name'], campus_id=campus_id))
            existing_buildings.add(building_key)

        if buildings_to_add:
            session.add_all(buildings_to_add)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def sync_rooms(room_list: list[dict[str, str]]) -> None:
    session = Session()
    try:
        existing_rooms = {
            (room.building_id, room.name)
            for room in session.query(Room).all()
        }
        building_ids = {
            (campus_name, building_name): building_id
            for building_id, building_name, campus_name in session.query(
                Building.id,
                Building.name,
                Campus.name,
            ).join(Campus, Building.campus_id == Campus.id).all()
        }

        rooms_to_add = []
        for room in room_list:
            building_id = building_ids.get((room['campus'], room['building']))
            if building_id is None:
                raise ValueError(
                    f"Unexpected building name: campus={room['campus']} building={room['building']}"
                )

            room_key = (building_id, room['name'])
            if room_key in existing_rooms:
                continue

            rooms_to_add.append(Room(name=room['name'], building_id=building_id))
            existing_rooms.add(room_key)

        if rooms_to_add:
            session.add_all(rooms_to_add)
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def sync_date_status(date: datetime, status: list) -> None:
    session = Session()
    try:
        rooms = {
            (building_name, room_name): room_id
            for room_id, room_name, building_name in session.query(
                Room.id,
                Room.name,
                Building.name,
            ).join(Building, Room.building_id == Building.id).all()
        }

        session.query(Status).filter_by(date=date.date()).delete()

        add_status = []
        for session_index, status in tqdm(enumerate(status)):
            session_index += 1
            for room in status:
                room_id = rooms.get((room['building'], room['room']))
                if room_id is None:
                    raise ValueError(
                        f"Unexpected room name: building={room['building']} room={room['room']}"
                    )
                add_status.append(Status(room_id=room_id, date=date, session_index=session_index))

        session.add_all(add_status)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_previous_record(date: datetime) -> None:
    session = Session()
    try:
        date = date.date()
        delete_num = session.query(Status).filter(Status.date < date).delete()
        print_flush(f"==> Deleted {delete_num} previous data")
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def sync_status(status: dict[datetime, list]) -> None:
    for date, status_list in status.items():
        print_flush("==> Syncing Status for date:", date.strftime("%Y-%m-%d"))
        sync_date_status(date, status_list)
