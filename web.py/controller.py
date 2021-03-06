#!/usr/bin/python

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
    '/bookCancel', 'bookCancel',
    '/take', 'take',
    '/checkTakeOk','checkTakeOk',
    '/getCloseBikes', 'getCloseBikes',
    '/bikeInaccessible','bikeInaccessible',
    '/getObsoleteReservations', 'getObsoleteReservations',
    '/getChangesBikes','getChangesBikes',
    '/getChangesUser','getChangesUser',
    '/checkResponseVelov', 'checkResponseVelov'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={ 'login_validated' : False,  'user_id' : 0, 'user_login': 0, 'firstname': 0, 'lastname': 0, 'email' : 0, 'tel_portable' : 0, 'velov_id' : 0, 'renting_session_start_time' : 0, 'renting_session_end_time' : 0, 'is_a_bike_in_use' : False, 'is_a_reservation_taking_place':False, 'reservation_starting_time':0, 'location_last_update_time' : 0, 'last_captured_latitude' : -1, 'last_captured_longitude' : -1 })

class index:
	def GET(self):		
		zones_interdites = model.getZoneInterdites()
		if authentication.is_logged(session) :
			print("the user is logged in")
			authentication.update_session(session)
			print session.__dict__
			return render.index(session, zones_interdites)
		else :
			print("the user is not logged in")
			authentication.logout(session) #clearing any remaining sessions
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
			if auth_results['login_validated'] == True :
				authentication.register_login(session,auth_results)
				view_msg ="successfully logged in"
				print session.__dict__
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
			task_id = model.bookVelo(session.user_id, i.velo)
			return task_id
		return "0"

class bookCancel:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			#TODO Selim : annuler reservation
			#pas d'argument car tu peux retrouver l'id du user avec la session et donc la reservation en cours
			return "OK"
		return "NO"

class take:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			i = web.input()
			task_id = model.takeVelo(session.user_id, i.velo)
			return task_id
		return "0"

class checkResponseVelov:
	def POST(self):
		web.header("Content-Type", "text/plain")
		i = web.input() 
		task_id = i.task_id
		if authentication.is_logged(session):
			status_code = model.getVeloTaskStatus(i.task_id)
			# Help:
			# -> 1 : 'todo' : 'Task to be picked up and processed.
			# -> 2 : 'inprogress' : 'The task is currently being processed / executed.
			# -> 3 : 'success' : 'The task has sucessfully completed.
			# -> 4 : 'failure' : 'The task could not be completed successfully.
			return status_code
		return "0"

class logout:
	def GET(self):
		authentication.logout(session)
		raise web.seeother('/')

class getCloseBikes:
	def POST(self):
		i = web.input()
		current_lat = 4 #i.current_location_lat #Not in use
		current_long = 45 #i.current_location_long #Not in use
		bikes = model.getCloseBikes(current_lat, current_long)
		tosend = list(bikes)
		web.header("Content-Type", "application/json")
		return json.dumps(tosend)

class getChangesBikes:
	def POST(self):
		web.header("Content-Type", "application/json")
		i = web.input() #on recupere le temps de rafraichissement comme ca je peux faire des tests avec plusieurs valeurs
		#Changement d'etat des velos
		time_slice=300 #TODO Chrarlotte: use i.time
		bikes_updates = model.getChangesBikes(time_slice)
		tosend = list(bikes_updates)
		return json.dumps(tosend)

class getChangesUser:
	def POST(self):
		web.header("Content-Type", "application/json")
		tosend=None
		if authentication.is_logged(session):
			authentication.update_session(session)
			tosend = session.__dict__
		return json.dumps(tosend)

class bikeInaccessible:
	def POST(self):
		web.header("Content-Type", "text/plain") 
		if authentication.is_logged(session):
			i = web.input()
			velo_id=i.velo
			model.signalBikeInaccessible(velo_id)
			return "OK"
		return "NO"

class getObsoleteReservations:
	def GET(self):
		results = model.getObsoleteReservations()
		tosend = list(results)
		web.header("Content-Type", "application/json")
		return json.dumps(tosend)

if __name__ == "__main__":
	app.run()
