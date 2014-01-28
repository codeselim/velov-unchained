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
		result = config.DB.select('user_action_history', query2_vars, where=" ($cur_timestamp - time) < 300 and action_id = 1 and user_id = $user_id order by time DESC limit 1 ")
		registration_taking_place=False
		print "hereeee1"
		if len(result) == 1 :
			reservation_taking_place=True
			reservation_start_time=result[0].time
			print "inside if"
		else :
			reservation_taking_place=False
			reservation_start_time=0
			print "inside else"
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
	# query = """ select vlh.velov_id as velov_id,
	# 			vlh.lat as velov_lat, vlh.long as velov_long,
	# 			vlh.time as location_history_time, vsh.time as state_history_time,
	# 			vsh.state_id as state_id, states.codename as state_codename, states.name as state_name 
	# 			from velov_state_history vsh, velov_location_history vlh, states
	# 			where vsh.velov_id = vlh.velov_id and states.id = vsh.state_id and vsh.state_id = 7 
	# 			order by vsh.time DESC """
	query = """ select vlhb.velov_id as velov_id,
				vlhb.lat as velov_lat, vlhb.long as velov_long,
				vlhb.time as location_history_time, vsha.time as state_history_time,
				vsha.state_id as state_id, states.codename as state_codename, states.name as state_name,
				velovs.inaccessibilty_report_nb as inaccessibilty_report_nb
				from
				(select vsh.velov_id as velov_id, vsh.time as time, state_id 
				from velov_state_history as vsh,  
				(select  max(vsh1.time) as time , vsh1.velov_id
				from velov_state_history vsh1
				where vsh1.state_id=7
				group by vsh1.velov_id) as vsh_cut
				where vsh.velov_id = vsh_cut.velov_id 
				and vsh_cut.time = vsh.time) as vsha
				,
				(select vlh.velov_id as velov_id, vlh.time as time, vlh.tile_index as tile_index, lat, long 
				from velov_location_history as vlh, 
				(select max(vlh1.time) as time, vlh1.velov_id
				from velov_location_history as vlh1
				group by vlh1.velov_id) as vlh_cut
				where vlh.velov_id = vlh_cut.velov_id 
				and vlh_cut.time = vlh.time) as vlhb
				,
				states , velovs
				where vsha.velov_id = vlhb.velov_id and states.id = vsha.state_id and vsha.state_id = 7 and vsha.velov_id = velovs.id
				order by vsha.time DESC """

	results = config.DB.query(query)
	return results

def getObsoleteReservations():
	query = """ 	SELECT * 
			FROM user_action_history
			WHERE ( (action_id=1) AND ( (EXTRACT( EPOCH FROM NOW() ) - time) > 300) ); """
	results = config.DB.query(query)
	tosend = list(results)
	print(tosend)
	return results

def signalBikeInaccessible(velov_id):
	query_string = " update velovs set inaccessibilty_report_nb = inaccessibilty_report_nb + 1 where id =	" + str(int(velov_id))+ " "
	result = config.DB.query(query_string)
	return result

def getChangesBikes(time_slice):
	current_timestamp = int(time.time())
	query_string = """ select vlh.velov_id as velov_id, vlh.time as time, vlh.state_id as state_id,
				states.codename as state_codename, states.name as state_name 
				from velov_state_history vlh, 
				states,
				(select max(time) as time, velov_id
				from velov_state_history 
				where ( """+str(int(current_timestamp))+""" - time) < """+time_slice+"""
				group by velov_id) as vsh_cut 
				where vlh.state_id = states.id and ( """+str(int(current_timestamp))+""" - vlh.time) < """+time_slice+"""
				and vsh_cut.time = vlh.time and vsh_cut.velov_id = vlh.velov_id """
	results = config.DB.query(query_string)
	return results

