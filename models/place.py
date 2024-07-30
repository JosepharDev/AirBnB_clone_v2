#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from os import getenv
import models
from models.amenity import Amenity
from models.review import Review

place_amenity = Table(
    "place_amenity",
    Base.metadata,
    Column("place_id", String(60), ForeignKey("places.id"),
           primary_key=True, nullable=False),
    Column("amenity_id", String(60), ForeignKey("amenities.id"),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """the place TABLE model

    class attributes:
        __tablename__ (string): Table name
        city_id (sting): The foreign city Id
        user_id (string): The foreign user Id
        name (string): The name of the place
        description (string): The description of the place
        number_rooms (integer): The number of rooms
        number_bathrooms (integer): The number of bathrooms
        max_guest (integer): The maximum number of guests
        price_by_night (integer): The price by night
        latitude (float): The latitude of the place
        longitude (float): The longitude of the place
        amenity_ids (list): The list of amenities ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", cascade='all, delete, delete-orphan',
                           backref="place")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False, back_populates="place_amenities")
    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """getter attribute reviews that returns the list of Review"""
            list_review = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    list_review.append(review)
            return list_review

        @property
        def amenities(self):
            """ Returns amenity ids"""
            list_amenity = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    list_amenity.append(amenity)
            return list_amenity

        @amenities.setter
        def amenities(self, value):
            if type(value) is Amenity and value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
