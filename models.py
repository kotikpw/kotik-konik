from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

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
    quiz_points = Column(Integer, default=0)
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
    active = Column(Boolean, nullable=False, default=False)

    def __init__(self, firstname, lastname, nickname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.email = email

    def get_profile_progress_in_percents(self):
        profile_points = 10
        total_profile_points = 85
        if self.avatar:
            profile_points += 10
        if self.university:
            profile_points += 5
        if self.faculty:
            profile_points += 5
        if self.year_of_study:
            profile_points += 5
        if self.github_username:
            profile_points += 15
        if self.reddit_username:
            profile_points += 15
        if self.linux_distribution:
            profile_points += 10
        if self.known_technologies:
            profile_points += 5
        if self.wants_to_learn:
            profile_points += 5
        return 100.0 * profile_points/total_profile_points

    def __repr__(self):
       fullname = "%s %s" % (self.firstname, self.lastname)
       return "<User('%s', '%s', '%s')>" % (fullname, self.nickname, self.email)

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answers = relationship("Answer")

    def __init__(self, question):
        self.question = question

    def __repr__(self):
       return "<Question('%i', '%s')>" % (self.id, self.question)

class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True)
    answer = Column(String, nullable=False)
    correct = Column(Boolean, nullable=False, default=False)
    question_id = Column(Integer, ForeignKey('questions.id'))

    def __init__(self, answer, correct):
	self.answer = answer
	self.correct = correct

    def __repr__(self):
       return "<Answer('%i', '%i')>" % (self.id, self.question_id)

users_table = User.__table__
questions_table = Question.__table__
answers_table = Answer.__table__
metadata = Base.metadata

if __name__ == "__main__":
    metadata.create_all(engine)
