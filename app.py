import web
from web import HTTPError
from web import application
from web import ctx as context
from web.contrib.template import render_jinja
from sqlalchemy.orm import scoped_session, sessionmaker
from base64 import b64decode

from models import *

urls = ('/', 'Home',
        '/register', 'Register',
        '/avatar/(.*)', 'Avatar')

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
        email = i.get('email')
        new_user = User(firstname, lastname, nickname, email)
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

class Avatar:
    def _avatar_as_bytestream_if_available(self, avatar):
        if avatar is not None:
            return self._avatar_as_bytestream(avatar)
        else:
            return self._empty_avatar_bytestream(avatar)

    def _empty_avatar_bytestream(self, avatar):
        default_avatar_file = open('static/img/unknown.png')
        default_avatar_bytes = default_avatar_file.read()
        return default_avatar_bytes

    def _avatar_as_bytestream(self, avatar):
        header_length = len("data:image/png;base64,")
        avatar_in_base64 = avatar[header_length:]
        avatar_bytes = b64decode(avatar_in_base64)
        return avatar_bytes

    def GET(self, nickname):
        avatar = None
        if nickname is not None:
            user = context.orm.query(User).filter_by(nickname=nickname).first()
            if user is not None:
                avatar = user.avatar
        web.header("Content-Type", "images/png")
        return self._avatar_as_bytestream_if_available(avatar)

app.add_processor(load_sqlalchemy)

if __name__ == "__main__":
    app.run()
