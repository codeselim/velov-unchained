#This file is the front controller
import web, model
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
		# pt1 = zones_interdites[0]
		# print pt1.lat
		# print pt1.long
		# pt2 = zones_interdites[1]
		# print pt2.lat
		# print pt2.long
		#print zones_interdites[0].long
		#check if the user is logged in
		zones_interdites = model.getZoneInterdites()
		if authentication.is_logged(session) :
			print("the user is logged in")
			return render.index(session, zones_interdites)
		else :
			print("the user is not logged in")
			return render.index(None, zones_interdites)

	def POST(self):
		zones_interdites = model.getZoneInterdites()
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
				return render.index(session, zones_interdites)
			else :
				view_msg ="Bad authentication"
				return render.index(None, zones_interdites)
		else :
			return render.index(None, zones_interdites)

class book:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			#TODO charlotte take the veloID from the post >> i = web.input() ...
			veloId=1
			model.bookVelo(session.user_id, veloId)
			return "OK"
		return "NO"

class take:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			#TODO charlotte take the veloID from the post >> i = web.input() ...
			veloId=1
			model.takeVelo(session.user_id, veloId)
			return "OK"
		return "NO"

class logout:
	def GET(self):
		authentication.logout(session)
		raise web.seeother('/')

if __name__ == "__main__":
	app.run()