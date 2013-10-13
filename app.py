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
        firstname = i.get('firstname')
        lastname = i.get('lastname')
        nickname = i.get('nickname')
        new_user = User(firstname, lastname, nickname)
        if i.has_key('avatar'):
            new_user.avatar = i.avatar
        if i.has_key('university'):
            new_user.university = i.university
        if i.has_key('faculty'):
            new_user.faculty = i.faculty
        if i.has_key('year'):
            new_user.year_of_study = i.year
        if i.has_key('github'):
            new_user.github_username = i.github
        if i.has_key('reddit'):
            new_user.reddit_username = i.reddit
        if i.has_key('unix'):
            new_user.linux_distribution = i.unix
        if i.has_key('iknow'):
            new_user.known_technologies = i.iknow
        if i.has_key('ineed'):
            new_user.wants_to_learn = i.ineed
        if i.has_key('imeet'):
            new_user.willingness_to_meet = i.imeet
        try:
            context.orm.add(new_user)
        except Exception, e:
            raise e
        return render.success()

app.add_processor(load_sqlalchemy)

if __name__ == "__main__":
    app.run()
