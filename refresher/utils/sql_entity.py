from sqlalchemy import String, BigInteger, Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Campus(Base):
    __tablename__ = 'campus'
    __table_args__ = (
        UniqueConstraint('name', name='uq_campus_name'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class Building(Base):
    __tablename__ = 'building'
    __table_args__ = (
        UniqueConstraint('campus_id', 'name', name='uq_building_campus_name'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    campus_id = Column(BigInteger, ForeignKey('campus.id'), nullable=False)


class Room(Base):
    __tablename__ = 'room'
    __table_args__ = (
        UniqueConstraint('building_id', 'name', name='uq_room_building_name'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    building_id = Column(BigInteger, ForeignKey('building.id'), nullable=False)


class Status(Base):
    __tablename__ = 'status'
    __table_args__ = (
        UniqueConstraint('room_id', 'date', 'session_index', name='uq_status_room_date_session'),
    )

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_id = Column(BigInteger, ForeignKey('room.id'), nullable=False)
    date = Column(Date, nullable=False)
    session_index = Column(Integer, nullable=False)
