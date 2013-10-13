import web
from web import HTTPError
from web import application
from web import ctx as context
from web.contrib.template import render_jinja
from sqlalchemy.orm import scoped_session, sessionmaker

from models import *

urls = ('/', 'Home',
        '/register', 'Register')

def load_sqlalchemy(handler):
    context.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except HTTPError:
       context.orm.commit()
       raise
    except:
        context.orm.rollback()
        raise
    finally:
        context.orm.commit()

app = application(urls, globals())
render = render_jinja('static', encoding = 'utf-8')

class Home:
    def GET(self):
        return render.index()

class Register:
    def POST(self):
        i = web.input()
        new_user = User(i.firstname, i.lastname, i.nickname)
        context.orm.add(new_user)
        return render.success()

app.add_processor(load_sqlalchemy)

if __name__ == "__main__":
    app.run()
