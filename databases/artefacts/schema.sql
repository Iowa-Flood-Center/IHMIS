--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.23
-- Dumped by pg_dump version 9.5.7

-- Started on 2017-12-07 17:43:20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2868 (class 1262 OID 1362250)
-- Name: artefacts; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE artefacts WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


\connect artefacts

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 9 (class 2615 OID 1362252)
-- Name: lookup; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA lookup;


--
-- TOC entry 10 (class 2615 OID 1362251)
-- Name: pois; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA pois;


--
-- TOC entry 8 (class 2615 OID 1362273)
-- Name: pois_dot; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA pois_dot;


--
-- TOC entry 1 (class 3079 OID 12648)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2870 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = lookup, pg_catalog;

--
-- TOC entry 189 (class 1255 OID 1365804)
-- Name: insert_usgsid_comid(text, integer); Type: FUNCTION; Schema: lookup; Owner: -
--

CREATE FUNCTION insert_usgsid_comid(usgs_id text, com_id integer) RETURNS boolean
    LANGUAGE plpgsql
    AS $$
DECLARE
  pois_id_var integer;
  pre_existing smallint;
BEGIN

  SELECT id FROM pois.pois_adv 
  WHERE foreign_id LIKE usgs_id INTO pois_id_var;

  -- 
  IF pois_id_var IS NULL THEN
    RAISE NOTICE 'No USGS ID found.';
    RETURN FALSE;
  END IF;

  -- 
  SELECT COUNT(*) FROM lookup.lookup_poisid_comid
  WHERE pois_id = pois_id_var INTO pre_existing;

  --
  IF pre_existing >= 1 THEN
    RAISE NOTICE 'Updating previous existing register.';
    UPDATE lookup.lookup_poisid_comid SET "comid" = com_id
    WHERE pois_id = pois_id_var;
  ELSE
    RAISE NOTICE 'Creating new register.';
    INSERT INTO lookup.lookup_poisid_comid(pois_id, comid)
    VALUES (pois_id_var, com_id);
  END IF;

  RETURN TRUE;
  
END;
$$;


SET default_with_oids = false;

--
-- TOC entry 176 (class 1259 OID 1365677)
-- Name: lookup_poisid_comid; Type: TABLE; Schema: lookup; Owner: -
--

CREATE TABLE lookup_poisid_comid (
    pois_id integer NOT NULL,
    comid integer NOT NULL
);


--
-- TOC entry 175 (class 1259 OID 1362713)
-- Name: lookup_poisid_linkid; Type: TABLE; Schema: lookup; Owner: -
--

CREATE TABLE lookup_poisid_linkid (
    pois_id integer NOT NULL,
    link_id integer
);


SET search_path = pois, pg_catalog;

--
-- TOC entry 173 (class 1259 OID 1362267)
-- Name: pois_adv; Type: TABLE; Schema: pois; Owner: -
--

CREATE TABLE pois_adv (
    id integer NOT NULL,
    foreign_id character varying(20),
    foreign_id1 character varying(20),
    lat numeric(9,6),
    lng numeric(9,6),
    n_lat numeric(9,6),
    n_lng numeric(9,6),
    state character(2),
    type integer,
    dwn_obj integer,
    lft bigint,
    rgt bigint,
    description character varying(100),
    kml_polygon character varying(100),
    kml_network character varying(100),
    population bigint,
    total_area double precision,
    upstream_area integer,
    travel_time integer,
    dist_border double precision,
    forecast integer,
    town character varying(100),
    river character varying(50),
    active boolean,
    association integer,
    x smallint,
    y smallint,
    rating_curve boolean,
    elevation real
);


--
-- TOC entry 2871 (class 0 OID 0)
-- Dependencies: 173
-- Name: TABLE pois_adv; Type: COMMENT; Schema: pois; Owner: -
--

COMMENT ON TABLE pois_adv IS 'The struct and content of this table is similar to the one returned by the WebService:

http://ifisfe.its.uiowa.edu/ifc/ifis.objects.php

except by the presence of the column link_id. This relationship is performed via tables in ''lookup'' schema';


SET search_path = pois_dot, pg_catalog;

--
-- TOC entry 174 (class 1259 OID 1362274)
-- Name: pois_adv_new; Type: TABLE; Schema: pois_dot; Owner: -
--

CREATE TABLE pois_adv_new (
    id integer,
    foreign_id character varying(20),
    foreign_id1 character varying(20),
    lat numeric(9,6),
    lng numeric(9,6),
    n_lat numeric(9,6),
    n_lng numeric(9,6),
    state character(2),
    type integer,
    dwn_link bigint,
    dwn_obj integer,
    lft bigint,
    rgt bigint,
    description character varying(100),
    kml_polygon character varying(100),
    kml_network character varying(100),
    population bigint,
    total_area double precision,
    upstream_area integer,
    travel_time integer,
    dist_border double precision,
    reading_time timestamp with time zone,
    last_reading double precision,
    warning integer,
    forecast_time timestamp with time zone,
    forecast integer,
    forecast_index double precision,
    town character varying(100),
    river character varying(50),
    time_now timestamp with time zone,
    active boolean,
    association integer,
    x smallint,
    y smallint,
    rating_curve boolean,
    elevation real
);


SET search_path = public, pg_catalog;

--
-- TOC entry 172 (class 1259 OID 1362261)
-- Name: pois_adv_new; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE pois_adv_new (
    id integer,
    foreign_id character varying(20),
    foreign_id1 character varying(20),
    lat numeric(9,6),
    lng numeric(9,6),
    n_lat numeric(9,6),
    n_lng numeric(9,6),
    state character(2),
    type integer,
    dwn_link bigint,
    dwn_obj integer,
    lft bigint,
    rgt bigint,
    description character varying(100),
    kml_polygon character varying(100),
    kml_network character varying(100),
    population bigint,
    total_area double precision,
    upstream_area integer,
    travel_time integer,
    dist_border double precision,
    reading_time timestamp with time zone,
    last_reading double precision,
    warning integer,
    forecast_time timestamp with time zone,
    forecast integer,
    forecast_index double precision,
    town character varying(100),
    river character varying(50),
    time_now timestamp with time zone,
    active boolean,
    association integer,
    x smallint,
    y smallint,
    rating_curve boolean,
    elevation real
);


SET search_path = lookup, pg_catalog;

--
-- TOC entry 2755 (class 2606 OID 1365681)
-- Name: pkey_lookup_poisid_comid; Type: CONSTRAINT; Schema: lookup; Owner: -
--

ALTER TABLE ONLY lookup_poisid_comid
    ADD CONSTRAINT pkey_lookup_poisid_comid PRIMARY KEY (pois_id);


--
-- TOC entry 2753 (class 2606 OID 1362717)
-- Name: pkey_lookup_poisid_linkid; Type: CONSTRAINT; Schema: lookup; Owner: -
--

ALTER TABLE ONLY lookup_poisid_linkid
    ADD CONSTRAINT pkey_lookup_poisid_linkid PRIMARY KEY (pois_id);


SET search_path = pois, pg_catalog;

--
-- TOC entry 2751 (class 2606 OID 1362285)
-- Name: pkey_pois_adv; Type: CONSTRAINT; Schema: pois; Owner: -
--

ALTER TABLE ONLY pois_adv
    ADD CONSTRAINT pkey_pois_adv PRIMARY KEY (id);


SET search_path = lookup, pg_catalog;

--
-- TOC entry 2756 (class 2606 OID 1365653)
-- Name: skey_pois_id; Type: FK CONSTRAINT; Schema: lookup; Owner: -
--

ALTER TABLE ONLY lookup_poisid_linkid
    ADD CONSTRAINT skey_pois_id FOREIGN KEY (pois_id) REFERENCES pois.pois_adv(id);


--
-- TOC entry 2757 (class 2606 OID 1365682)
-- Name: skey_pois_id; Type: FK CONSTRAINT; Schema: lookup; Owner: -
--

ALTER TABLE ONLY lookup_poisid_comid
    ADD CONSTRAINT skey_pois_id FOREIGN KEY (pois_id) REFERENCES pois.pois_adv(id);


-- Completed on 2017-12-07 17:43:21

--
-- PostgreSQL database dump complete
--

