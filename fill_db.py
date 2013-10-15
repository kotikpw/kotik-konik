from models import *
from sqlalchemy.orm import scoped_session, sessionmaker
from web import ctx as context
from web import HTTPError

context.orm = scoped_session(sessionmaker(bind=engine))

q = Question('Kto stworzyl jezyk programowania C?')
q.answers = [
	Answer('James Gosling', 0),
	Answer('Bjarne Stroustrup', 0),
	Answer('Dennis Ritchie', 1),
	Answer('Anders Hejlsberg', 0)
	]

context.orm.add(q)
context.orm.commit()

