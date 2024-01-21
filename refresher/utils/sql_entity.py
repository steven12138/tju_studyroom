from sqlalchemy import String, BigInteger, Column, Integer, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Campus(Base):
    __tablename__ = 'campus'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)


class Building(Base):
    __tablename__ = 'building'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    campus_id = Column(BigInteger, nullable=False)


class Room(Base):
    __tablename__ = 'room'
    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    building_id = Column(BigInteger, nullable=False)


class Status(Base):
    __tablename__ = 'status'
    id = Column(BigInteger, primary_key=True)
    room_id = Column(BigInteger, nullable=False)
    date = Column(Date, nullable=False)
    session_index = Column(Integer, nullable=False)
