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
	session.velov_id = auth_data['velov_id']
	session.renting_session_start_time = auth_data['renting_session_start_time']
	session.renting_session_end_time = auth_data['renting_session_end_time']
	session.location_last_update_time = auth_data['location_last_update_time']
	session.last_captured_latitude = auth_data['last_captured_latitude']
	session.last_captured_longitude = auth_data['last_captured_longitude']
	session.is_a_bike_in_use= auth_data['is_a_bike_in_use']
	session.is_a_reservation_taking_place = auth_data['is_a_reservation_taking_place']
	session.reservation_starting_time = auth_data['reservation_starting_time']

def update_session(session):
	_vars = dict(login=session.user_login)
	updated_data = model.getSessionUpdates(_vars)
	register_login(session, updated_data)

def logout(session):
	session.login_validated = False
	session.kill()