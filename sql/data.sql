INSERT INTO tasks_types (id, name) VALUES (1, "Change state to Unlockable");
INSERT INTO tasks_types (id, name) VALUES (2, "Change state to Available");
INSERT INTO tasks_types (id, name) VALUES (3, "Change state to Not Available");
INSERT INTO tasks_types (id, name) VALUES (4, "Change state to Not Available");
INSERT INTO tasks_types (id, name) VALUES (5, "Change state to In Maintenance");


SELECT pg_catalog.setval('task_types_id_seq', 6, true);