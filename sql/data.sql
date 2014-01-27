\c velovunchained

INSERT INTO task_types (id, name) VALUES (1, 'Change state to Unlockable');
INSERT INTO task_types (id, name) VALUES (2, 'Change state to Available');
INSERT INTO task_types (id, name) VALUES (3, 'Change state to Unusable');
INSERT INTO task_types (id, name) VALUES (4, 'Change state to In Use');
INSERT INTO task_types (id, name) VALUES (5, 'Change state to Off');
INSERT INTO task_types (id, name) VALUES (6, 'Change state to Reserved');

SELECT pg_catalog.setval('task_types_id_seq', 6, true);

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
VALUES (1, 'selimabisaber', '12345678', now(), FALSE, 'selim', 'saber', 'm', '2000-08-24 14:00:00', '20 Avenue xyz', '69100', 'Villeurbanne', 'selimabisaber@gmail.com', '614184746', '2014-08-24 16:00:00' );
INSERT INTO users ( id, login, password, creation_date, is_disabled, firstname, lastname, sex, birth_date, address, code_postal, ville, email, tel_portable, membership_exipry_date) 
VALUES (2, 'test', 'test', now(), FALSE, 'MyFirstname', 'MyLastname', 'f', '1988-02-24 13:00:00', '2 Avenue xyz', '69003', 'Lyon', 'selimabisaber@gmail.com', '614184746', '2015-08-24 16:00:00' );

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

SELECT pg_catalog.setval('states_id_seq', 6, true);
-- ---------------------------------------------- --------------------------------------

INSERT INTO velovs (id) VALUES (1);
INSERT INTO velovs (id) VALUES (2);
INSERT INTO velovs (id) VALUES (3);
INSERT INTO velovs (id) VALUES (4);
INSERT INTO velovs (id) VALUES (5);

SELECT pg_catalog.setval('velovs_id_seq', 6, true);
-- ---------------------------------------------- --------------------------------------

INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 1, 1, CURRENT_TIMESTAMP);
INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 2, 2, CURRENT_TIMESTAMP);
INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 1, 2, 2, CURRENT_TIMESTAMP);
INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 2, 1, 3, CURRENT_TIMESTAMP);
INSERT INTO velov_tasks (task_state_id , type, user_id, velov_id, action_time) VALUES (1, 2, 2, 4, CURRENT_TIMESTAMP);

-- ---------------------------------------

INSERT INTO user_action_history (action_id, user_id, velov_id, time) VALUES (2, 1, 1, 1390492193016);
