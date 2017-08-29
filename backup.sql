--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.21
-- Dumped by pg_dump version 9.5.8

-- Started on 2017-08-30 00:32:26 +07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 11733)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1938 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 513 (class 1247 OID 16388)
-- Name: statuses; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE statuses AS ENUM (
    'DRAFT',
    'FULFILLMENT',
    'CANCELED',
    'COMPLETED'
);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 170 (class 1259 OID 16399)
-- Name: orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE orders (
    id integer NOT NULL,
    contact_name character varying(200),
    contact_phone character varying(100),
    contact_email character varying(150),
    status statuses NOT NULL,
    created timestamp without time zone NOT NULL,
    confirmed timestamp without time zone,
    comment text,
    price numeric(9,2)
);


--
-- TOC entry 169 (class 1259 OID 16397)
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE orders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 1939 (class 0 OID 0)
-- Dependencies: 169
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE orders_id_seq OWNED BY orders.id;


--
-- TOC entry 1820 (class 2604 OID 16402)
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY orders ALTER COLUMN id SET DEFAULT nextval('orders_id_seq'::regclass);


--
-- TOC entry 1825 (class 2606 OID 16407)
-- Name: orders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 1821 (class 1259 OID 16410)
-- Name: ix_orders_confirmed; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_orders_confirmed ON orders USING btree (confirmed);


--
-- TOC entry 1822 (class 1259 OID 16408)
-- Name: ix_orders_created; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_orders_created ON orders USING btree (created);


--
-- TOC entry 1823 (class 1259 OID 16409)
-- Name: ix_orders_status; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_orders_status ON orders USING btree (status);


-- Completed on 2017-08-30 00:32:36 +07

--
-- PostgreSQL database dump complete
--
