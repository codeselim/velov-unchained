# -*- coding: utf-8 -*-
import psycopg2

#Connection to database
conn = psycopg2.connect("dbname=velovunchained user=velovunchained password=velovunchained")
#Cursor used to navigate through the database
cur = conn.cursor()


#Reads the id of the last reservation action tested for the warning rules application
last_action_read = 0
with open("last_action_read.txt", "r") as my_file:
	last_action_read = my_file.read().strip()


#This query get all reservation older than 5 minutes
query = """ 	SELECT user_id,velov_id,time,id
		FROM user_action_history
		WHERE ( ( id>%s ) AND (action_id=1) AND ( (EXTRACT( EPOCH FROM NOW() ) - time) > 300) ); """

cur.execute(query,last_action_read)
#we store the results of the query in results ( it's a tuple of tuples )
results = cur.fetchall()

#Every line is a transaction of the query's result
for line in results:
	user_id = line[0]
	velov_id = line[1]
	time = line[2]
	resa_id = line[3]
	last_action_read = resa_id 
	#this query looks for an "unlock operation" happening less than 5 minutes after the reservation
	myQuery = """ 	SELECT * 
					FROM user_action_history 
					WHERE ( (action_id=2) AND (user_id= %s ) AND (velov_id= %s) AND ( (time - %s) < 300) AND ( (time - %s) >0 ) ) """
	cur.execute(myQuery,(user_id,velov_id,time,time))
	res = cur.fetchall()
	if not res:
		print("Blame pour l'utiisateur {0} pour la réservation d'id {1}".format(user_id,resa_id))
		#This query insert a warning for this user in the database
		warningQuery = """	INSERT INTO user_warning_history (user_id, action_history_id) VALUES (%s, %s);"""
		cur.execute(warningQuery, (user_id,resa_id))
		#Make the change persistent in the database
		conn.commit()

			
	else:
		print("Reservation OK pour l'utiisateur {0} pour la réservation d'id {1} du vélo {2}".format(user_id,resa_id,velov_id))
	last_action_read = resa_id 
with open("last_action_read.txt","w") as my_file:
	#update the last_action_read file
	my_file.write(str(last_action_read))
cur.close()