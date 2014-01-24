import model

def authenticate(variables):
	return model.authenticate(variables) #returns true if the user has the right , not disabled

def is_logged(session):
	if session.login_validated == True:
		return True
	else:
		return False

def register_login(session,auth_data):
	session.login_validated = auth_data['login_validated']
	session.user_id= auth_data['user_id']
	session.user_login= auth_data['user_login']
	session.firstname=auth_data['firstname']
	session.lastname=auth_data['lastname']
	session.email=auth_data['email']
	session.tel_portable=auth_data['tel_portable']

def logout(session):
	session.login_validated = False
	session.kill()