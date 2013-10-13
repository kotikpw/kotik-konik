from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///kotik.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    nickname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    avatar = Column(String)
    university = Column(String)
    faculty = Column(String)
    year_of_study = Column(Integer)
    github_username = Column(String)
    reddit_username = Column(String)
    linux_distribution = Column(String)
    known_technologies = Column(String)
    wants_to_learn = Column(String)
    willingness_to_attend_meetings = Column(String)

    def __init__(self, firstname, lastname, nickname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.email = email

    def __repr__(self):
       fullname = "%s %s" % (self.firstname, self.lastname)
       return "<User('%s','%s', '%s', '%s')>" % (fullname, self.nickname, self.email)


users_table = User.__table__
metadata = Base.metadata


if __name__ == "__main__":
    metadata.create_all(engine)
