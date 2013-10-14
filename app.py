# -*- encoding: utf-8
import web
import urllib2
from web import HTTPError
from web import application
from web import ctx as context
from web.contrib.template import render_jinja
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import IntegrityError
from base64 import b64decode

from models import *

prefix = '/konik'
urls = ('/', 'RedirectHome', prefix, 'RedirectHome',
        prefix + '/', 'Home',
        prefix + '/register', 'Register',
        prefix + '/quiz', 'Quiz',
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

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def check_url(url):
    request = HeadRequest(url)
    response = urllib2.urlopen(request)
    valid = response.getcode() == 200
    if not valid:
        print "Response code: %d" % response.getcode()
    return valid

def check_github_username(github_username):
    if check_url('https://github.com/%s' % github_username):
        return True
    return False

def check_reddit_username(reddit_username):
    if check_url('http://www.reddit.com/user/%s' % reddit_username):
        return True
    return False

def check_linux_distribution(linux_distribution):
    if check_url('http://distrowatch.com/table.php?distribution=%s' % linux_distribution):
        return True
    return False

def empty_or_none(value, default=None):
    if not value or not len(value):
        return default
    return value

def percents(value):
    return '%.0f%%' % value

app = application(urls, globals())
wsgi = app.wsgifunc()
render = render_jinja('static', encoding = 'utf-8')
render._lookup.filters.update({'percents':percents})

class RedirectHome:
    def GET(self):
        raise web.seeother(prefix + '/')

class Home:
    def GET(self):
        return render.registration()

class Register:
    def POST(self):
        i = web.input()
        firstname = empty_or_none(i.get('firstname'), default='Andrzej')
        lastname = empty_or_none(i.get('lastname'), default='Molibdenowy')
        nickname = empty_or_none(i.get('nickname'), default='nie_wiadomo_kto')
        email = empty_or_none(i.get('email'))
        info = []

	new_user = context.orm.query(User).filter_by(email=email).filter_by(active=False).first()
	if new_user == None:
	    new_user = User(firstname, lastname, nickname, email)
	else:
	    new_user.firstname = firstname
	    new_user.lastname = lastname
	    new_user.nickname = nickname
	    new_user.email = email
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
            if check_github_username(i.github):
                info.append(u"Dodatkowe punkty za konto na GitHubie!")
        if i.has_key('reddit'):
            new_user.reddit_username = i.reddit
            if check_reddit_username(i.reddit):
                info.append(u"Dodatkowe punkty za konto na reddit!")
        if i.has_key('unix'):
            new_user.linux_distribution = i.unix
            if check_linux_distribution(i.unix):
                info.append(u"Dodatkowe punkty za konto na używanie %s!" % i.unix)
        if i.has_key('iknow'):
            new_user.known_technologies = i.iknow
        if i.has_key('ineed'):
            new_user.wants_to_learn = i.ineed
        if i.has_key('imeet'):
            new_user.willingness_to_meet = i.imeet
	new_user.active = True
	profile_progress = new_user.get_profile_progress_in_percents()
        
        try:
            context.orm.add(new_user)
            context.orm.commit()
        except IntegrityError, e:
            context.orm.rollback()
            if email is None:
                return render.registration(errors=[u"Podaj adres e-mail"])
            else:
                return render.registration(errors=[u"Podany e-mail jest już zajęty"])
        return render.success(firstname=firstname, lastname=lastname, nickname=nickname, email=email, \
				successes=[u"Witaj %s!" % nickname], info=info, \
				profile_progress=profile_progress)

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

class Quiz:
    limit = 10

    def generate_quesions(self):
	full_list = context.orm.query(Question).all()
	shuffle(full_list)
	return full_list[:self.limit]

    def GET(self):
	question_list = self.generate_quesions()
        return render.quiz(question_list=question_list)

    def POST(self):
        i = web.input(answer=[])
        nickname = i.get('nickname')
        email = i.get('email')
        
	user = context.orm.query(User).filter_by(email=email).first()
	if user is None:
		user = User('', '', nickname, email)

        user.quiz_points = 0  
	user.given_answers = []
        
        form_keys = i.keys()

	for question_key in form_keys:
		question_id = None
		try:
			question_id = int(question_key)
		except Exception:
			pass

		if question_id is None:
			continue

		question = context.orm.query(Question).filter_by(id=question_id).first()
		if question is None:
			continue

		all_correct = True
		for answer_key in i.get(question_key):
			try:
				answer_id = int(answer_key)
			except Exception:
				pass

			if answer_id is None:
				all_correct = False
				continue

                        answer = context.orm.query(Answer).filter_by(id=answer_id).first()
                        if answer is None or answer.correct == False:
				all_correct = False

		if all_correct:
			user.quiz_points += 10
	
	context.orm.add(user)
	return render.quiz(question_list=i.get('answer'))

app.add_processor(sqlalchemy_processor)

if __name__ == "__main__":
    app.run()
