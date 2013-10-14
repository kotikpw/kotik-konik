from models import *
from sqlalchemy.orm import scoped_session, sessionmaker
from web import ctx as context
from web import HTTPError

context.orm = scoped_session(sessionmaker(bind=engine))

q = Question('Czy zawadzki jest czepialski?')
q.answers = [Answer('Tak', 1), Answer('Nie', 0), Answer('Moze', 0)]

context.orm.add(q)
context.orm.commit()


