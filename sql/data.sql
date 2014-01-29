\c velovunchained

INSERT INTO task_types (id, name) VALUES (1, 'Change state to Unlockable');
INSERT INTO task_types (id, name) VALUES (2, 'Change state to Available');
INSERT INTO task_types (id, name) VALUES (3, 'Change state to Unusable');
INSERT INTO task_types (id, name) VALUES (4, 'Change state to In Use');
INSERT INTO task_types (id, name) VALUES (5, 'Change state to Off');
INSERT INTO task_types (id, name) VALUES (6, 'Change state to Reserved');

SELECT pg_catalog.setval('task_types_id_seq', 7, true);

-- ---------------------------------------------- --------------------------------------

INSERT INTO states (id, codename, name) VALUES (1, 'UNK', 'Unknown');
INSERT INTO states (id, codename, name) VALUES (2, 'USE', 'In use');
INSERT INTO states (id, codename, name) VALUES (3, 'STO', 'Stolen');
INSERT INTO states (id, codename, name) VALUES (4, 'UNU', 'Unused');
INSERT INTO states (id, codename, name) VALUES (5, 'RES', 'Reserved');
INSERT INTO states (id, codename, name) VALUES (6, 'UNL', 'Unlockable');
INSERT INTO states (id, codename, name) VALUES (7, 'AVA', 'Available');
INSERT INTO states (id, codename, name) VALUES (8, 'OFF', 'Off');

SELECT pg_catalog.setval('states_id_seq', 9, true);

-- ---------------------------------------------- --------------------------------------

INSERT INTO task_states (id, codename, name) VALUES (1, 'todo', 'Task to be picked up and processed');
INSERT INTO task_states (id, codename, name) VALUES (2, 'inprogress', 'The task is currently being processed / executed.');
INSERT INTO task_states (id, codename, name) VALUES (3, 'success', 'The task has sucessfully completed.');
INSERT INTO task_states (id, codename, name) VALUES (4, 'failure', 'The task could not be completed successfully.');


SELECT pg_catalog.setval('task_types_id_seq', 5, true);

-- ---------------------------------------------- --------------------------------------
INSERT INTO users ( id, login, password, creation_date, is_disabled, firstname, lastname, sex, birth_date, address, code_postal, ville, email, tel_portable, membership_exipry_date) 
VALUES (1, 'test', 'test', 1390492193016, FALSE, 'selim', 'saber', 'm', '2000-08-24 14:00:00', '20 Avenue xyz', '69100', 'Villeurbanne', 'selimabisaber@gmail.com', '614184746', 1453900731 );
INSERT INTO users ( id, login, password, creation_date, is_disabled, firstname, lastname, sex, birth_date, address, code_postal, ville, email, tel_portable, membership_exipry_date) 
VALUES (2, 'test2', 'test2', 1390492193016, FALSE, 'Jane', 'Smith', 'f', '1988-02-24 13:00:00', '2 Avenue xyz', '69003', 'Lyon', 'selimabisaber@gmail.com', '614184746', 1453900731 );
INSERT INTO users ( id, login, password, creation_date, is_disabled, firstname, lastname, sex, birth_date, address, code_postal, ville, email, tel_portable, membership_exipry_date) 
VALUES (3, 'test3', 'test3', 1390492193016, FALSE, 'Markus', 'Muller', 'm', '1988-02-24 13:00:00', '2 Avenue xyz', '69003', 'Lyon', 'selimabisaber@gmail.com', '614184746', 1453900731 );

SELECT pg_catalog.setval('users_id_seq', 3, true);

-- ---------------------------------------------- --------------------------------------

INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.854326, 45.772552);
INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.85836, 45.772911);
INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.85939, 45.784764);
INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.852009, 45.783626 );
INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.847374, 45.780873 );
INSERT INTO zones_interdites (id, long, lat) VALUES (1, 4.844885, 45.777371 );

SELECT pg_catalog.setval('zones_interdites_id_seq', 2, true);

-------------------------------------------------------------------------------
INSERT INTO user_actions (id, name) VALUES (1, 'Reservation');
INSERT INTO user_actions (id, name) VALUES (2, 'Unlock authorization');
INSERT INTO user_actions (id, name) VALUES (3, 'Unlock action');
INSERT INTO user_actions (id, name) VALUES (4, 'Lock authorization');
INSERT INTO user_actions (id, name) VALUES (5, 'Lock action');
INSERT INTO user_actions (id, name) VALUES (6, 'Cancel Reservation');

SELECT pg_catalog.setval('states_id_seq', 6, true);
-- ---------------------------------------------- --------------------------------------

INSERT INTO velovs (id) VALUES (1);
INSERT INTO velovs (id) VALUES (2);
INSERT INTO velovs (id) VALUES (3);
INSERT INTO velovs (id) VALUES (4);
INSERT INTO velovs (id) VALUES (5);
INSERT INTO velovs (id) VALUES (6);
INSERT INTO velovs (id) VALUES (7);
INSERT INTO velovs (id) VALUES (8);
INSERT INTO velovs (id) VALUES (9);
INSERT INTO velovs (id) VALUES (10);
INSERT INTO velovs (id) VALUES (11);
INSERT INTO velovs (id) VALUES (12);
INSERT INTO velovs (id) VALUES (13);
INSERT INTO velovs (id) VALUES (14);
INSERT INTO velovs (id) VALUES (15);

SELECT pg_catalog.setval('velovs_id_seq', 16, true);
-- ---------------------------------------------- --------------------------------------

-- INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 1, 1, 1390828731);
-- INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 2, 2, 1390828731);
-- INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 2, 2, 1390828731);

-- ---------------------------------------

INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (1, 2, 1, 1390828731); --julien, ordre chronologique 	 	
INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (1, 1, 12, 1390828761); --julien
INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (2, 1, 12, 1390828771); --julien
INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (1, 2, 1, 1390829771); --julien
INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (2, 1, 1, 1390828731);
INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (1, 3, 2, 1390931697); -- user test3 id 3 is reserving with action id 1 the bike id 2 that was AVA

---------------------------------------------
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (1, 1, 1390828731, 7);  -- bike id=1 IN USE
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (2, 2, 1390828731, 7);  -- charlotte's veloPCV01 AVA
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (3, 3, 1390828731, 7);  -- charlotte's veloPCV02 AVA --> recent timestamp
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (4, 3, 1390820732, 2);  -- charlotte's veloPCV02 IN USE
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (5, 3, 1390822733, 2);  -- charlotte's veloPCV02 IN USE
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (6, 4, 1390828731, 7);  -- charlotte's veloPCV03 AVA
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (7, 7, 1390901876, 2);  -- bike id=7 IN USE
INSERT INTO velov_state_history (id,  velov_id, time, state_id) VALUES (8, 7, 1390820780, 7);  -- bike id=7 was AVA
SELECT pg_catalog.setval('velov_state_history_id_seq', 9, true);
---------------------------------------------------
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (1,1,1390828746, 1, 45.7728813, 4.87606287);
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (2,2,1390828770, 1, 45.75, 4.85); -- charlotte's veloPCV01
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (3,3,1390828771, 1, 45.76, 4.85); -- charlotte's veloPCV02
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (4,3,1390822772, 1, 46.33, 4.87); -- charlotte's veloPCV02
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (5,3,1390820773, 1, 46.22, 4.84); -- charlotte's veloPCV02
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (6,4,1390828790, 1, 45.75, 4.86); -- charlotte's veloPCV03
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (7,7,1390901874, 1, 46.44, 4.86); -- bike id 7
INSERT INTO velov_location_history(id, velov_id, time, tile_index,lat, long  ) VALUES (8,7,1390820780, 1, 44.7728813, 4.86); -- bike id 7
SELECT pg_catalog.setval('velov_location_history_id_seq', 9, true);
-------------------------------------------------------------------------

-- INSERT INTO user_renting_sessions(id, user_id, velov_id, time_start, time_end) VALUES (1, 2, 7, 1390901720, NULL); -- renting session still running
-- INSERT INTO user_renting_sessions(id, user_id, velov_id, time_start, time_end) VALUES (2, 3, 6, 1390824631, 1390826631); -- renting session already ended
-- SELECT pg_catalog.setval('user_renting_sessions_id_seq', 3, true);
