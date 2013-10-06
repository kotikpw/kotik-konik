import web
from web.contrib.template import render_jinja

urls = ('/(.*)', 'Home')

app = web.application(urls, globals())
render = render_jinja('static', encoding = 'utf-8')

class Home:
    def GET(self, name):
        return render.index(name=name)

if __name__ == "__main__":
    app.run()
