from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from Configurations.config import Base
# without having declerative base or base sqlalchemy wont
# know which class is a database table

from sqlalchemy.schema import PrimaryKeyConstraint

# Define your models here
class Topics(Base):
    __tablename__ = "topics"
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(45))
    title = Column(String(150))
    release_date = Column(Date)
    artist_name = Column(String(100))
    genre = Column(String(45))

    progress = relationship("Progress", back_populates="topics")
    # back populate allows us to work with both tables without using joins.
    # still uses joins under the hood.

    def __repr__(self):
        return f"{self.topic_id},{self.type},{self.title},{self.release_date}, {self.artist_name}, {self.genre}"

class Progress(Base):
    __tablename__ = "progress"
    user_id = Column(Integer, ForeignKey('user.user_id'))
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    completed = Column(Boolean)
    not_started = Column(Boolean)
    in_progress = Column(Boolean)

    #composite primary key
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'topic_id'),  
    )
    user = relationship("User", back_populates="progress")
    topics = relationship("Topics", back_populates="progress")

    def __repr__(self):
        return f"{self.user_id},{self.topic_id},{self.completed},{self.not_started}, {self.in_progress}"

    def update_progress(self, completed,not_started,in_progress,session):
        self.completed=completed
        self.not_started=not_started
        self.in_progress=in_progress
        session.add(self)
        session.commit()
 
        self.__repr__()


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    password = Column(String(45))
    role = Column(String(10), default='user')
    progress = relationship("Progress", back_populates="user")

    def __repr__(self):
        return f"{self.user_id},{self.name},{self.role},{self.password}"
