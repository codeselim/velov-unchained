#This file is the front controller
import web
import authentication
import view, config
from view import render

web.config.debug = False

urls = (
    '/', 'index',
    '/logout', 'logout',
    '/book', 'book'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'otherVar': 0, 'name': None, 'id': None})

class index:
	def GET(self):
		#check if the user is logged in
		if authentication.is_logged(session) :
			print("the user is logged in")
			#TODO if the user is logged-in we should display the logout
			return render.index(session)
		else :
			print("the user is not logged in")
			return render.index(None)

	def POST(self):
		print("POST Submitted")
		i = web.input()
		# We received a POST from the login form
		if i.submitlogin != None :
			postVars = dict(login=i.login, password=i.password)
			auth_results = authentication.authenticate(postVars)
			#TODO (Selim) : renvoyer l'ID de l'util ou pas si on se base sur login ?
			print(auth_results)
			if auth_results == True:
				authentication.register_login(session,i.login)
				print session._initializer
				view_msg ="successfully logged in"
				print(i) #printing the post vars
				return render.index(session)
			else :
				view_msg ="Bad authentication"
				#view_msg should be sent to the view
				return render.index(None)
		
class book:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			#modifier etat de l'util en reservation + compteur pour 5min
			return "OK"
		return "NO"

class logout:
	def GET(self):
		authentication.logout(session)
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()