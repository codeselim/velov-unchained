import config

#def listing(**k):
#    return config.DB.select('items', **k)

def authenticate(variables):
	#@TODO Hash the password
	#@TODO add to the query a membership expiry date check
	entries = config.DB.select('users', variables, where="login=$login and password=$password and is_disabled=FALSE")
	nb_entries = len(entries)
	if nb_entries == 1 :
		return True
	else :
		return False