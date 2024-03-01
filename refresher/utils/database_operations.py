import os
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from .sql_entity import Campus, Building, Room, Status
from .util import print_flush

database_name = os.getenv("DATABASE", 'studyroom')
database_user = os.getenv("SQL_USER", 'studyroom')
database_password = os.getenv("SQL_PASS", '123456')
database_url = os.getenv("SQL_URL", 'localhost')
database_port = os.getenv("SQL_PORT", '3306')

engine = create_engine(
    f'mysql+pymysql://{database_user}:{database_password}@{database_url}:{database_port}/{database_name}')

Session = sessionmaker(bind=engine)
session = Session()


def check_connection() -> None:
    global session, Session, engine
    for i in range(3):
        try:
            session.execute(text('SELECT 1'))
            return
        except Exception as e:
            print_flush("==> Connection Error")
            print_flush(e)
            print_flush("==> Refresh Connection Session, retrying:", i + 1, "/3")
            engine = create_engine(
                f'mysql+pymysql://{database_user}:{database_password}@{database_url}:{database_port}/{database_name}')
            Session = sessionmaker(bind=engine)
            session = Session()

    print_flush("==> Failed to connect to database")
    raise


def sync_campus(campuses: list[str]):
    existing_campuses = set(session.query(Campus.name).all())

    new_campuses = [Campus(name=name) for name in campuses if (name,) not in existing_campuses]

    if new_campuses:
        session.add_all(new_campuses)
        session.commit()


def sync_buildings(buildings: list[dict[str, str]]) -> None:
    existing_building_names = set(session.query(Building.name).all())

    campus_ids = {campus.name: campus.id for campus in session.query(Campus).all()}

    new_buildings = [b for b in buildings if (b['name'],) not in existing_building_names]

    buildings_to_add = []
    for building in new_buildings:
        campus_id = campus_ids.get(building['campus'])
        if campus_id:
            buildings_to_add.append(Building(name=building['name'], campus_id=campus_id))
        else:
            # TODO: log error
            assert False, "Unexpected campus name: " + building['campus']

    if buildings_to_add:
        session.add_all(buildings_to_add)
        session.commit()


def sync_rooms(room_list: list[dict[str, str]]) -> None:
    exist_room_names = set(session.query(Room.name).all())

    building_ids = {building.name: building.id for building in session.query(Building).all()}

    new_rooms = [r for r in room_list if (r['name'],) not in exist_room_names]
    rooms_to_add = []
    for room in new_rooms:
        building_id = building_ids.get(room['building'])
        if building_id:
            rooms_to_add.append(Room(name=room['name'], building_id=building_id))
        else:
            assert False, "Unexpected building name: " + room['building']

    if rooms_to_add:
        session.add_all(rooms_to_add)
        session.commit()


def sync_date_status(date: datetime, status: list) -> None:
    rooms = {room.name: room for room in session.query(Room).all()}

    session.query(Status).filter_by(date=date.date()).delete()
    add_status = []
    for session_index, status in tqdm(enumerate(status)):
        session_index += 1
        for room in status:
            room = rooms.get(room['room'])
            if room:
                add_status.append(Status(room_id=room.id, date=date, session_index=session_index))
            else:
                assert False, "Unexpected room name: " + room['room']

    session.add_all(add_status)
    session.commit()


def delete_previous_record(date: datetime) -> None:
    date = date.date()
    session.query(Status).filter(Status.date < date).delete()
    session.commit()


def sync_status(status: dict[datetime, list]) -> None:
    for date, status_list in status.items():
        print_flush("==> Syncing Status for date:", date.strftime("%Y-%m-%d"))
        sync_date_status(date, status_list)
