import config
import web
import tools
import time
#def listing(**k):
#    return config.DB.select('items', **k)

def authenticate(variables):
	current_timestamp = int(time.time())
	#@TODO Hash the password
	#@TODO add to the query a membership expiry date check
	query = """ select u.id as id, u.login as login, u.firstname as firstname, u.lastname as lastname, 
				u.email as email, u.tel_portable as tel_portable, 
				urs.velov_id as velov_id, urs.time_start as renting_session_start_time,
				urs.time_end as renting_session_end_time, vlh.time as location_last_update_time, 
				vlh.lat as last_captured_latitude, vlh.long as last_captured_longitude
				From users u
				left join user_renting_sessions urs
				on u.id = urs.user_id 
				left join velov_location_history vlh 
				on vlh.velov_id = urs.velov_id
				where u.login='"""+variables['login']+"""' and u.password='"""+variables['password']+"""' and u.is_disabled=FALSE 
				order by vlh.time DESC limit 1 """
	entries = config.DB.query(query)
	
	# entries = config.DB.select('users', variables, where="login=$login and password=$password and is_disabled=FALSE")
	nb_entries = len(entries)
	if nb_entries == 1 :
		row = entries[0]
		query2_vars = dict(cur_timestamp=current_timestamp, user_id=row.id)
		result = config.DB.select('user_action_history', query2_vars, where=" (time - $cur_timestamp) < 300 and action_id = 1 and user_id = $user_id order by time DESC limit 1 ")
		registration_taking_place=False
		if len(result) == 1 :
			reservation_taking_place=True
			reservation_start_time=result[0].time
		else :
			reservation_taking_place=False
			reservation_start_time=0

		bike_in_use=False
		if row.renting_session_end_time  == None :
			bike_in_use=True
		else :
			bike_in_use=False
		result =  dict(login_validated=True, user_id=row.id,  user_login=row.login, firstname=row.firstname, lastname=row.lastname, email=row.email, tel_portable=row.tel_portable, velov_id=row.velov_id, renting_session_start_time=row.renting_session_start_time, renting_session_end_time=row.renting_session_end_time, is_a_bike_in_use=bike_in_use, is_a_reservation_taking_place=reservation_taking_place, reservation_starting_time=reservation_start_time, location_last_update_time=row.location_last_update_time, last_captured_latitude=row.last_captured_latitude, last_captured_longitude=row.last_captured_longitude)
		return result
	else :
		return dict(login_validated=False, user_id=0,  user_login=0, firstname=0, lastname=0, email=0, tel_portable=0, velov_id=0, renting_session_start_time=0, renting_session_end_time=None, is_a_bike_in_use=False, is_a_reservation_taking_place=False, reservation_starting_time=0, last_captured_latitude=-1, last_captured_longitude=-1 )

def takeVelo(userID, veloID):
	current_timestamp = int(time.time())
	sequence_id = config.DB.insert('velov_tasks', task_state_id=1, type=1, user_id=userID, velov_id=veloID, action_time=current_timestamp);

def bookVelo(userID, veloID):
	current_timestamp = int(time.time())
	sequence_id = config.DB.insert('velov_tasks', task_state_id=1, type=6, user_id=userID, velov_id=veloID, action_time=current_timestamp);	

def getZoneInterdites():
	entries = config.DB.select('zones_interdites')
	return entries

def getCloseBikes(current_lat, current_long):
	tile_index = tools.tileIndex(current_lat, current_long)
	search_depth = 3
	tile_indexes = tools.zonePerimeter(tile_index, search_depth) #@TODO use tileindex in fetching bikes... 
	query = """ select vlh.velov_id as velov_id,
				vlh.lat as velov_lat, vlh.long as velov_long,
				vlh.time as location_history_time, vsh.time as state_history_time,
				vsh.state_id as state_id, states.codename as state_codename, states.name as state_name 
				from velov_state_history vsh, velov_location_history vlh, states
				where vsh.velov_id = vlh.velov_id and states.id = vsh.state_id and vsh.state_id = 7 
				order by vsh.time DESC """
	results = config.DB.query(query)
	return results

def getObsoleteReservations():
	query = """ SELECT * FROM velov_tasks
				WHERE ( (type=2) AND ( (EXTRACT( EPOCH FROM NOW() ) - action_time) > 300) ); """
	results = config.DB.query(query)
	return results
