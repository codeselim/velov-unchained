--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;


CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE task_types (
    id integer NOT NULL,
    name character(10)
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

-- --------------------------------- ---------------------------------
CREATE TABLE velov_tasks (
    id integer NOT NULL,
    type integer NOT NULL
);
ALTER TABLE public.velov_tasks OWNER TO velovunchained;
CREATE SEQUENCE velov_tasks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE ONLY task_types ADD CONSTRAINT task_types_pk PRIMARY KEY (id);
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT tasks_pk PRIMARY KEY (id);
ALTER TABLE public.velov_tasks_id_seq OWNER TO velovunchained;
ALTER SEQUENCE velov_tasks_id_seq OWNED BY velov_tasks.id;
ALTER TABLE ONLY velov_tasks ADD CONSTRAINT task_type_fk FOREIGN KEY (type) REFERENCES task_types(id);
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
    id integer NOT NULL
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

-- --
-- -- Name: id; Type: DEFAULT; Schema: public; Owner: velovunchained
-- --



-- --
-- -- Name: id; Type: DEFAULT; Schema: public; Owner: velovunchained
-- --


--
-- Data for Name: task_types; Type: TABLE DATA; Schema: public; Owner: velovunchained
--

-- COPY task_types (id, name) FROM stdin;
-- 1    Hey       
-- 2    Hey       
-- \.


-- --
-- -- Name: task_types_id_seq; Type: SEQUENCE SET; Schema: public; Owner: velovunchained
-- --

-- SELECT pg_catalog.setval('task_types_id_seq', 2, true);


-- --
-- -- Data for Name: velov_tasks; Type: TABLE DATA; Schema: public; Owner: velovunchained
-- --

-- COPY velov_tasks (id, type) FROM stdin;
-- 7	1
-- \.


-- --
-- -- Name: velov_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: velovunchained
-- --

-- SELECT pg_catalog.setval('velov_tasks_id_seq', 7, true);


-- --
-- -- Name: task_types_pk; Type: CONSTRAINT; Schema: public; Owner: velovunchained; Tablespace: 
-- --


-- --
-- -- Name: public; Type: ACL; Schema: -; Owner: postgres
-- --

-- REVOKE ALL ON SCHEMA public FROM PUBLIC;
-- REVOKE ALL ON SCHEMA public FROM postgres;
-- GRANT ALL ON SCHEMA public TO postgres;
-- GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

