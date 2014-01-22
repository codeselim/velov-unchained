#This file is the front controller
import web
import authentication
import view, config
from view import render

web.config.debug = False

urls = (
    '/', 'index',
    'logout', 'logout'
    'login', 'login'
)

app = web.application(urls, globals())
app.internalerror = web.debugerror
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'otherVar': 0})

class index:
	def GET(self):
		#check if the user is logged in
		if authentication.is_logged(session) :
			print("the user is logged in")
			#TODO if the user is logged-in we should display the logout
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
			print(auth_results)
			if auth_results == True:
				authentication.register_login(session)
				view_msg ="successfully logged in"
				#view_msg should be sent to the view
			else :
				view_msg ="Bad authentication"
				#view_msg should be sent to the view
		print(i) #printing the post vars
		util = "Charlotte"
		return render.index(util)

if __name__ == "__main__":
	app.run()


# class logout:
# 	def GET(self):
# 		authentication.logout(session)