INSERT INTO task_types (id, name) VALUES (1, 'Change state to Unlockable');
INSERT INTO task_types (id, name) VALUES (2, 'Change state to Available');
INSERT INTO task_types (id, name) VALUES (3, 'Change state to Not Available');
INSERT INTO task_types (id, name) VALUES (4, 'Change state to Not Available');
INSERT INTO task_types (id, name) VALUES (5, 'Change state to In Maintenance');

SELECT pg_catalog.setval('task_types_id_seq', 6, true);

-- ---------------------------------------------- --------------------------------------

INSERT INTO task_states (id, codename, name) VALUES (1, 'todo', 'Task to be picked up and processed');
INSERT INTO task_states (id, codename, name) VALUES (2, 'inprogress', 'The task is currently being processed / executed.');
INSERT INTO task_states (id, codename, name) VALUES (3, 'success', 'The task has sucessfully completed.');
INSERT INTO task_states (id, codename, name) VALUES (4, 'failure', 'The task could not be completed successfully.');


SELECT pg_catalog.setval('task_types_id_seq', 5, true);