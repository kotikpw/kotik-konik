import web
from web.contrib.template import render_jinja

urls = ('/', 'Home',
        '/register', 'Register')

app = web.application(urls, globals())
render = render_jinja('static', encoding = 'utf-8')

class Home:
    def GET(self):
        return render.index()

class Register:
    def POST(self):
        i = web.input()
        print i.firstname
        print i.avatar
        return render.success()

if __name__ == "__main__":
    app.run()
