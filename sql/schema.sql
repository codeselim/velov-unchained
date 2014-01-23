--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE IF EXISTS velovunchained;
CREATE DATABASE velovunchained;
GRANT ALL PRIVILEGES ON DATABASE velovunchained TO velovunchained;
commit;
\c velovunchained;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;
-- --------------------------------------------------------------
-- --------------------------------------------------------------


CREATE TABLE users (
    id bigint NOT NULL,
    login varchar(120) NOT NULL,
    password varchar(120) NOT NULL,
    creation_date TIMESTAMP NOT NULL DEFAULT NOW(),
    is_disabled BOOLEAN DEFAULT FALSE,
    firstname varchar(120) NOT NULL,
    lastname varchar(120) NOT NULL,
    sex char(1) NOT NULL,
    birth_date DATE NOT NULL,
    address varchar(220) NOT NULL,
    code_postal varchar(10) NOT NULL,
    ville varchar(45) NOT NULL,
    email varchar(100) NOT NULL,
    tel_portable integer NOT NULL,
    tel_secondaire integer NULL,
    membership_exipry_date TIMESTAMP NOT NULL
);
ALTER TABLE public.users OWNER TO velovunchained;
CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.users_id_seq OWNER TO velovunchained;
ALTER SEQUENCE users_id_seq OWNED BY users.id;
ALTER TABLE ONLY users ADD CONSTRAINT users_pk PRIMARY KEY (id);
ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

-- --------------------------------- ---------------------------------


CREATE TABLE task_types (
    id integer NOT NULL,
    name varchar(100) NOT NULL
);
ALTER TABLE public.task_types OWNER TO velovunchained;
CREATE SEQUENCE task_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.task_types_id_seq OWNER TO velovunchained;
ALTER SEQUENCE task_types_id_seq OWNED BY task_types.id;
ALTER TABLE ONLY task_types ALTER COLUMN id SET DEFAULT nextval('task_types_id_seq'::regclass);
ALTER TABLE ONLY task_types ADD CONSTRAINT task_types_pk PRIMARY KEY (id);

-- --------------------------------- ---------------------------------

CREATE TABLE task_states (
    id integer NOT NULL,
    codename varchar(20) NOT NULL,
    name varchar(100) NOT NULL
);
ALTER TABLE public.task_states OWNER TO velovunchained;
CREATE SEQUENCE task_states_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY task_states ADD CONSTRAINT tasks_states_pk PRIMARY KEY (id);
ALTER TABLE public.task_states_id_seq OWNER TO velovunchained;
ALTER SEQUENCE task_states_id_seq OWNED BY task_states.id;
ALTER TABLE ONLY task_states ALTER COLUMN id SET DEFAULT nextval('task_states_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE velov_tasks (
    id integer NOT NULL,
    type integer NOT NULL,
    user_id integer, --  This column can be NULL because a task can be not related to a user (set to unusuable / maintenance, for instance (unless we have special users for maintenance guys... will see))
    velov_id integer NOT NULL,
    task_state_id integer NOT NULL
);
ALTER TABLE public.velov_tasks OWNER TO velovunchained;
CREATE SEQUENCE velov_tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT tasks_pk PRIMARY KEY (id);
ALTER TABLE public.velov_tasks_id_seq OWNER TO velovunchained;
ALTER SEQUENCE velov_tasks_id_seq OWNED BY velov_tasks.id;
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT task_type_fk FOREIGN KEY (type) REFERENCES task_types(id);
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT task_state_id_fk FOREIGN KEY (task_state_id) REFERENCES task_states(id);
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT velov_id_fk FOREIGN KEY (velov_id) REFERENCES velovs(id);
ALTER TABLE ONLY velov_tasks ALTER COLUMN id SET DEFAULT nextval('velov_tasks_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE velovs (
    id integer NOT NULL
);
ALTER TABLE public.velovs OWNER TO velovunchained;
CREATE SEQUENCE velovs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.velovs_id_seq OWNER TO velovunchained;
ALTER SEQUENCE velovs_id_seq OWNED BY velovs.id;
ALTER TABLE ONLY velovs ADD CONSTRAINT velovs_pk PRIMARY KEY (id);
ALTER TABLE ONLY velovs ALTER COLUMN id SET DEFAULT nextval('velovs_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE velov_location_history (
    id integer NOT NULL,
    velov_id integer NOT NULL,
    time bigint NOT NULL,
    tile_index integer NOT NULL,
    lat double precision NOT NULL,
    long double precision NOT NULL
);
ALTER TABLE public.velov_location_history OWNER TO velovunchained;
CREATE SEQUENCE velov_location_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.velov_location_history_id_seq OWNER TO velovunchained;
ALTER SEQUENCE velov_location_history_id_seq OWNED BY velov_location_history.id;
ALTER TABLE ONLY velov_location_history ADD CONSTRAINT velov_location_history_pk PRIMARY KEY (id);
ALTER TABLE ONLY velov_location_history ADD CONSTRAINT velov_loc_velov_id_fk FOREIGN KEY (velov_id) REFERENCES velovs(id);
ALTER TABLE ONLY velov_location_history ALTER COLUMN id SET DEFAULT nextval('velov_location_history_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE states (
    id integer NOT NULL,
    codename char(3) NOT NULL,
    name varchar(100) NOT NULL
);
ALTER TABLE public.states OWNER TO velovunchained;
CREATE SEQUENCE states_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.states_id_seq OWNER TO velovunchained;
ALTER SEQUENCE states_id_seq OWNED BY states.id;
ALTER TABLE ONLY states ADD CONSTRAINT states_pk PRIMARY KEY (id);
ALTER TABLE ONLY states ALTER COLUMN id SET DEFAULT nextval('states_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE velov_state_history (
    id integer NOT NULL,
    velov_id integer NOT NULL,
    time bigint NOT NULL,
    state_id integer NOT NULL
);
ALTER TABLE public.velov_state_history OWNER TO velovunchained;
CREATE SEQUENCE velov_state_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.velov_state_history_id_seq OWNER TO velovunchained;
ALTER SEQUENCE velov_state_history_id_seq OWNED BY velov_state_history.id;
ALTER TABLE ONLY velov_state_history ADD CONSTRAINT velov_state_history_pk PRIMARY KEY (id);
ALTER TABLE ONLY velov_state_history ADD CONSTRAINT velov_state_history_velov_id_fk FOREIGN KEY (velov_id) REFERENCES velovs(id);
ALTER TABLE ONLY velov_state_history ADD CONSTRAINT velov_state_history_state_id_fk FOREIGN KEY (state_id) REFERENCES states(id);
ALTER TABLE ONLY velov_state_history ALTER COLUMN id SET DEFAULT nextval('velov_state_history_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE user_actions (
    id integer NOT NULL,
    name varchar(100) NOT NULL
);
ALTER TABLE public.user_actions OWNER TO velovunchained;
CREATE SEQUENCE user_actions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.user_actions_id_seq OWNER TO velovunchained;
ALTER SEQUENCE user_actions_id_seq OWNED BY user_actions.id;
ALTER TABLE ONLY user_actions ADD CONSTRAINT user_actions_pk PRIMARY KEY (id);
ALTER TABLE ONLY user_actions ALTER COLUMN id SET DEFAULT nextval('user_actions_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE user_action_history (
    id integer NOT NULL,
    user_id integer NOT NULL,
    velov_id integer NOT NULL,
    time bigint NOT NULL,
    action_id integer NOT NULL
);
ALTER TABLE public.user_action_history OWNER TO velovunchained;
CREATE SEQUENCE user_action_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.user_action_history_id_seq OWNER TO velovunchained;
ALTER SEQUENCE user_action_history_id_seq OWNED BY user_action_history.id;
ALTER TABLE ONLY user_action_history ADD CONSTRAINT user_action_history_pk PRIMARY KEY (id);
ALTER TABLE ONLY user_action_history ADD CONSTRAINT user_action_history_velov_id_fk FOREIGN KEY (velov_id) REFERENCES velovs(id);
ALTER TABLE ONLY user_action_history ADD CONSTRAINT user_action_history_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE ONLY user_action_history ADD CONSTRAINT user_action_history_state_id_fk FOREIGN KEY (action_id) REFERENCES user_actions(id);
ALTER TABLE ONLY user_action_history ALTER COLUMN id SET DEFAULT nextval('user_action_history_id_seq'::regclass);

-- --------------------------------- ---------------------------------

CREATE TABLE user_renting_sessions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    velov_id integer NOT NULL,
    time_start bigint DEFAULT NULL,
    time_end bigint DEFAULT NULL
);
ALTER TABLE public.user_renting_sessions OWNER TO velovunchained;
CREATE SEQUENCE user_renting_sessions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE public.user_renting_sessions_id_seq OWNER TO velovunchained;
ALTER SEQUENCE user_renting_sessions_id_seq OWNED BY user_renting_sessions.id;
ALTER TABLE ONLY user_renting_sessions ADD CONSTRAINT user_renting_sessions_pk PRIMARY KEY (id);
ALTER TABLE ONLY user_renting_sessions ADD CONSTRAINT user_renting_sessions_velov_id_fk FOREIGN KEY (velov_id) REFERENCES velovs(id);
ALTER TABLE ONLY user_renting_sessions ADD CONSTRAINT user_renting_sessions_user_id_fk FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE ONLY user_renting_sessions ADD CONSTRAINT user_renting_sessions_state_id_fk FOREIGN KEY (action_id) REFERENCES user_actions(id);
ALTER TABLE ONLY user_renting_sessions ALTER COLUMN id SET DEFAULT nextval('user_renting_sessions_id_seq'::regclass);

-- --------------------------------- ---------------------------------
