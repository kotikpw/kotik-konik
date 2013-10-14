# -*- encoding: utf-8
import web
from web import HTTPError
from web import application
from web import ctx as context
from web.contrib.template import render_jinja
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from base64 import b64decode

from models import *

prefix = '/konik'
urls = (prefix + '/', 'Home',
        prefix + '/register', 'Register',
        prefix + '/avatar/(.*)', 'Avatar')

def sqlalchemy_processor(handler):
    # after handling a request we are autocommiting all changes
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
wsgi = app.wsgifunc()
render = render_jinja('static', encoding = 'utf-8')

class Home:
    def GET(self):
        return render.index_sea()

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
            context.orm.commit()
        except IntegrityError, e:
            context.orm.rollback()
            return render.index(error=u"Podany e-mail jest już zajęty")
        return render.success(email=email)

class Avatar:
    def _avatar_as_bytestream_if_available(self, avatar):
        if avatar is not None and len(avatar) > 0:
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

    def GET(self, email):
        avatar = None
        if email is not None:
            user = context.orm.query(User).filter_by(email=email).first()
            if user is not None:
                avatar = user.avatar
        web.header("Content-Type", "image/png")
        web.header("Content-Disposition", "attachment;filename=\"%s\"" % 'avatar.png')
        return self._avatar_as_bytestream_if_available(avatar)

app.add_processor(sqlalchemy_processor)

if __name__ == "__main__":
    app.run()
