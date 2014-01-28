#This file is the front controller
import web, model
import authentication
import view, config
import json
import time
from view import render

web.config.debug = False

urls = (
    '/', 'index',
    '/logout', 'logout',
    '/book', 'book',
    '/take', 'take',
    '/getCloseBikes', 'getCloseBikes',
    '/getObsoleteReservations', 'getObsoleteReservations'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={ 'login_validated' : False,  'user_id' : 0, 'user_login': 0, 'firstname': 0, 'lastname': 0, 'email' : 0, 'tel_portable' : 0, 'velov_id' : 0, 'renting_session_start_time' : 0, 'renting_session_end_time' : 0, 'location_last_update_time' : 0, 'last_captured_latitude' : -1, 'last_captured_longitude' : -1 })

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
			i = web.input()
			model.bookVelo(session.user_id, i.velo)
			return "OK"
		return "NO"

class take:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			i = web.input()
			model.takeVelo(session.user_id, i.velo)
			return "OK"
		return "NO"

class logout:
	def GET(self):
		authentication.logout(session)
		raise web.seeother('/')

class getCloseBikes:
	def POST(self):
		#i = web.input()
		#current_lat = i.current_location_lat
		#current_long = i.current_location_long
		current_lat = 45.767433
		current_long = 4.875676
		bikes = model.getCloseBikes(current_lat, current_long)
		tosend = list(bikes)
		web.header("Content-Type", "application/json")
		return json.dumps(tosend)

class getObsoleteReservations:
	def GET(self):
		results = model.getObsoleteReservations()
		tosend = list(results)
		web.header("Content-Type", "application/json")
		return json.dumps(tosend)


if __name__ == "__main__":
	app.run()