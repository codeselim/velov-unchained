#This file is the front controller
import web

import view, config
from view import render

urls = (
    '/', 'index',
#    'test', 'test'
)

class index:
	def GET(self):
		return render.index(None)
	def POST(self):
		#TODO check couple login/pwd
		util = "Charlotte"
		return render.index(util)

class test:
	def GET(self):
		return render.base()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror
    app.run()
