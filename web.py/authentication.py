import model

def authenticate(variables):
	return model.authenticate (variables) #returns true if the user has the right , not disabled

def is_logged(session):
	if session.login == 1:
		return True
	else:
		return False

def register_login(session,name):
	session.login = 1
	session.name = name

def logout(session):
	session.login = 0
	session.kill()