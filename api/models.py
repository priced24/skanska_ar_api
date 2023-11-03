from datetime import datetime
from typing import List
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Building(Base):
    """ Building

    Model class representing a Building data source.
    """
    __tablename__ = "building"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    rooms: Mapped[List["Room"]] = relationship(
        "Room", back_populates="building", foreign_keys="Room.building_id", cascade='all, delete')

    __mapper_args__ = {'polymorphic_identity': 'building'}

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        """ __repr__

        String representation of the Building instance
        """
        return f'<Building(id={self.id},name={self.name!r})>'

    def __str__(self):
        """ __str__

        Display string of Building
        """
        return f'Building {self.name}'

    def to_json(self):
        """ to_json

        Serializes the Building instance as a JSON object, where each key/value
        pair corresponds to the Building's fields.
        """
        room_json = [room.to_json() for room in self.rooms]
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "rooms": room_json
        }


class Room(Base):
    """ Room

    Model class representing a Room data source.
    """
    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    sensors: Mapped[List["Sensor"]] = relationship(
        "Sensor", back_populates="room", foreign_keys="Sensor.room_id", cascade='all, delete')
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))
    building: Mapped["Building"] = relationship(
        back_populates="rooms", foreign_keys=building_id, cascade='all, delete')

    __mapper_args__ = {'polymorphic_identity': 'room'}

    def __init__(self, name=None, description=None, building_id=None):
        self.name = name
        self.description = description
        self.building_id = building_id

    def __repr__(self):
        """ __repr__

        String representation of the Room instance
        """
        return f'<Room(id={self.id},name={self.name})>'

    def __str__(self):
        """ __str__

        Display string of Room
        """
        return f'Room {self.name}'

    def to_json(self):
        """ to_json

        Serializes the Room instance to a JSON object, where each key/value
        pair corresponds to the Room's fields.
        """
        sensor_json = [sensor.to_json() for sensor in self.sensors]
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "building": self.building.name,
            "building_id": self.building_id,
            "sensors": sensor_json
        }


class Sensor(Base):
    """ Sensor

    Model class representing a Sensor data source.
    """
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    data: Mapped[List["SensorDataReadable"]] = relationship(
        "SensorDataReadable", back_populates="sensor", foreign_keys="SensorDataReadable.sensor_id", cascade='all, delete')
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"))
    room: Mapped["Room"] = relationship(
        back_populates="sensors", foreign_keys=room_id, cascade='all, delete')

    __mapper_args__ = {'polymorphic_identity': 'sensor'}

    def __init__(self, name=None, description=None, room_id=None):
        self.name = name
        self.description = description
        self.room_id = room_id

    def __repr__(self):
        """ __repr__

        String representation of the Sensor instance
        """
        return f'<Sensor(id={self.id},name={self.name})>'

    def __str__(self):
        """ __str__

        Display string of Sensor
        """
        return f'Sensor {self.name}'

    def to_json(self):
        """ to_json

        Serializes the Sensor instance to a JSON object, where each key/value
        pair corresponds to the Sensor's fields.
        """

        # This will need to change to prevent "dumping" a large partition of the database into JSON
        data_json = [data.to_json() for data in self.data]
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "room": self.room.name,
            "room_id": self.room_id,
            "data": data_json
        }


class SensorDataReadable(Base):
    """ SensorDataReadable

    Model class representing a sensor datum.
    """
    __tablename__ = "sensor_data_readable"

    id = Column(Integer, primary_key=True)
    value = Column(String(255), nullable=False)
    units = Column(String(255), nullable=False)
    datetime = Column(DateTime, nullable=False)
    sensor_id: Mapped[int] = mapped_column(ForeignKey("sensor.id"))
    sensor: Mapped["Sensor"] = relationship(
        back_populates="data", foreign_keys=sensor_id, cascade='all, delete')

    __mapper_args__ = {'polymorphic_identity': 'sdr'}

    def __init__(self, sensor_id=None, value=None, units=None, datetime=None):
        self.sensor_id = sensor_id
        self.value = value
        self.units = units
        self.datetime = datetime

    def __repr__(self):
        """ __repr__

        String representation of the SensorDataReadable instance
        """
        return f'<SensorDataReadable(id={self.id},name={self.name})>'

    def __str__(self):
        """ __str__

        Display string of SensorDataReadable instance
        """
        return f'SensorDataReadable {self.value} {self.type}'

    def to_json(self):
        """ to_json

        Serializes the SensorDataReadable to a JSON object, where each key/value
        pair corresponds to the SensorDataReadable instance's fields.
        """

        # Avoid circular import
        from .constants import DATETIME_FORMAT_STRING

        return {
            "id": self.id,
            "sensor": self.sensor.name,
            "sensor_id": self.sensor_id,
            "value": self.value,
            "units": self.units,
            "datetime": datetime.strftime(self.datetime, DATETIME_FORMAT_STRING)
        }
