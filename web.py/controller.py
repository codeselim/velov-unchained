#This file is the front controller
import web
import authentication
import view, config
from view import render

web.config.debug = False

urls = (
    '/', 'index',
    '/logout', 'logout',
    '/book', 'book',
    '/take', 'take'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={ 'login_validated' : False,  'user_id' : 0, 'user_login': 0, 'firstname': 0, 'lastname': 0, 'email' : 0, 'tel_portable' : 0})

class index:
	def GET(self):
		#check if the user is logged in
		if authentication.is_logged(session) :
			print("the user is logged in")
			return render.index(session)
		else :
			print("the user is not logged in")
			return render.index(None)

	def POST(self):
		print("POST Submitted")
		i = web.input()
		print(i) #printing the post vars
		# We received a POST from the login form
		if i.submitlogin != None :
			postVars = dict(login=i.login, password=i.password)
			auth_results = authentication.authenticate(postVars)
			# print(auth_results)
			if auth_results['login_validated'] == True:
				authentication.register_login(session,auth_results)
				view_msg ="successfully logged in"
				return render.index(session)
			else :
				view_msg ="Bad authentication"
				return render.index(None)
		else :
			return render.index(None)

class book:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			model.book(UserId, veloId) #modifier etat de l'util en reservation + compteur pour 5min
			velov_tasks
			return "OK"
		return "NO"

class take:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			#enregistrer dans la BDD
			return "OK"
		return "NO"

class logout:
	def GET(self):
		authentication.logout(session)
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()