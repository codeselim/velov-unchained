import config
import web
import tools

#def listing(**k):
#    return config.DB.select('items', **k)

def authenticate(variables):
	#@TODO Hash the password
	#@TODO add to the query a membership expiry date check
	entries = config.DB.select('users', variables, where="login=$login and password=$password and is_disabled=FALSE")
	nb_entries = len(entries)
	if nb_entries == 1 :
		row = entries[0]
		result =  dict(login_validated=True, user_id=row.id,  user_login=row.login, firstname=row.firstname, lastname=row.lastname, email=row.email, tel_portable=row.tel_portable)
		return result
	else :
		return dict(login_validated=False, user_id=0,  user_login=0, firstname=0, lastname=0, email=0, tel_portable=0)

def takeVelo(userID, veloID):
	sequence_id = config.DB.insert('velov_tasks', task_state_id=1, type=1, user_id=userID, velov_id=veloID, action_time=web.SQLLiteral("CURRENT_TIMESTAMP"));

def bookVelo(userID, veloID):
	sequence_id = config.DB.insert('velov_tasks', task_state_id=1, type=6, user_id=userID, velov_id=veloID, action_time=web.SQLLiteral("CURRENT_TIMESTAMP"));	

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
				where vsh.velov_id = vlh.velov_id and states.id = vsh.state_id and vsh.state_id = 7 """
	results = config.DB.query(query)
	return results



