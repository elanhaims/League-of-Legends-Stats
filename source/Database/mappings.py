from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Game(Base):
    __tablename__ = 'games'

    id = Column(String, primary_key=True)
    date = Column(DateTime)
    duration = Column(Integer)
    won = Column(Boolean)
    participants = relationship("Participant", back_populates="game")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(String, primary_key=True)
    summoner_name = Column(String)
    champion = Column(String)
    won = Column(Boolean)
    kills = Column(Integer)
    deaths = Column(Integer)
    damage = Column(Integer)
    pentakills = Column(Integer)
    quadrakills = Column(Integer)
    game_id = Column(String, ForeignKey('games.id'))
    game = relationship("Game", back_populates="participants")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
