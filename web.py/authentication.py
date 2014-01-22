import model

def authenticate(variables):
	return model.authenticate (variables) #returns true if the user has the right , not disabled

def is_logged(session):
	if session.login == 1:
		return True
	else:
		return False

def register_login(session):
	session.login = 1

def logout(session):
	session.login = 0
	session.kill()