--
-- PostgreSQL database dump
--

-- Dumped from database version 11.14 (Debian 11.14-1.pgdg90+1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

DROP SCHEMA IF EXISTS public CASCADE;

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: audittype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.audittype AS ENUM (
    'comments',
    'status_change',
    'type_change',
    'milestone_change',
    'assignee_change'
);


ALTER TYPE public.audittype OWNER TO postgres;

--
-- Name: roles; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.roles AS ENUM (
    'customer',
    'lead',
    'developer'
);


ALTER TYPE public.roles OWNER TO postgres;

SET default_tablespace = '';

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: audit_issue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_issue (
    audit_id integer NOT NULL,
    issue_id integer NOT NULL,
    previous_status_id integer,
    updated_status_id integer,
    previous_type_id integer,
    updated_type_id integer,
    previous_milestone_id integer,
    updated_milestone_id integer,
    comments character varying,
    audit_type public.audittype NOT NULL,
    attachment_url character varying[],
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer NOT NULL,
    previous_assignee_id integer,
    updated_assignee_id integer
);


ALTER TABLE public.audit_issue OWNER TO postgres;

--
-- Name: audit_issue_audit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_issue_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.audit_issue_audit_id_seq OWNER TO postgres;

--
-- Name: audit_issue_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_issue_audit_id_seq OWNED BY public.audit_issue.audit_id;


--
-- Name: issue_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issue_status (
    issue_status_id integer NOT NULL,
    status character varying
);


ALTER TABLE public.issue_status OWNER TO postgres;

--
-- Name: issue_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issue_types (
    issue_type_id integer NOT NULL,
    type character varying,
    type_description character varying
);


ALTER TABLE public.issue_types OWNER TO postgres;

--
-- Name: issues; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issues (
    issue_id integer NOT NULL,
    issue_title character varying NOT NULL,
    issue_description character varying,
    project_id integer NOT NULL,
    type_id integer,
    status_id integer,
    priority_id integer,
    milestone_id integer,
    module_id integer,
    gitlab_issue_id integer,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    created_by integer NOT NULL,
    attachment_url character varying[],
    assigned_to integer
);


ALTER TABLE public.issues OWNER TO postgres;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.projects (
    project_id integer NOT NULL,
    project_name character varying,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.projects OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    organization_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    is_superuser boolean,
    created_on timestamp without time zone DEFAULT now() NOT NULL,
    user_role public.roles NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: audit_view; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.audit_view AS
 SELECT audit.audit_view_type,
    audit.issue_id,
    audit.issue_title,
    audit.type_id,
    audit.type_name,
    audit.status_id,
    audit.status_name,
    audit.project_id,
    audit.project_name,
    audit.audit_id,
    audit.audit_type,
    audit.previous_status_id,
    audit.previous_status_name,
    audit.updated_status_id,
    audit.updated_status_name,
    audit.previous_type_id,
    audit.previous_type_name,
    audit.updated_type_id,
    audit.updated_type_name,
    audit.comments,
    audit.created_on,
    audit.created_by,
    audit.created_by_name
   FROM ( SELECT 'issue'::text AS audit_view_type,
            issue.issue_id,
            issue.issue_title,
            issue.type_id,
            issue_types.type AS type_name,
            issue.status_id,
            issue_status.status AS status_name,
            issue.project_id,
            projects.project_name,
            NULL::integer AS audit_id,
            NULL::public.audittype AS audit_type,
            NULL::integer AS previous_status_id,
            NULL::character varying AS previous_status_name,
            NULL::integer AS updated_status_id,
            NULL::character varying AS updated_status_name,
            NULL::integer AS previous_type_id,
            NULL::character varying AS previous_type_name,
            NULL::integer AS updated_type_id,
            NULL::character varying AS updated_type_name,
            NULL::character varying AS comments,
            issue.created_on,
            issue.created_by,
            concat(users.first_name, ' ', users.last_name) AS created_by_name
           FROM ((((public.issues issue
             JOIN public.users ON ((issue.created_by = users.user_id)))
             JOIN public.projects ON ((issue.project_id = projects.project_id)))
             LEFT JOIN public.issue_types ON ((issue.type_id = issue_types.issue_type_id)))
             LEFT JOIN public.issue_status ON ((issue.status_id = issue_status.issue_status_id)))
        UNION
         SELECT 'audit_issue'::text AS audit_view_type,
            ai.issue_id,
            issues.issue_title,
            NULL::integer AS type_id,
            NULL::character varying AS type_name,
            NULL::integer AS status_id,
            NULL::character varying AS status_name,
            issues.project_id,
            projects.project_name,
            ai.audit_id,
            ai.audit_type,
            ai.previous_status_id,
            previous_status.status AS previous_status_name,
            ai.updated_status_id,
            updated_status.status AS updated_status_name,
            ai.previous_type_id,
            previous_type.type AS previous_type_name,
            ai.updated_type_id,
            updated_type.type AS updated_type_name,
            ai.comments,
            ai.created_on,
            ai.created_by,
            concat(users.first_name, ' ', users.last_name) AS created_by_name
           FROM (((((((public.audit_issue ai
             JOIN public.issues ON ((ai.issue_id = issues.issue_id)))
             JOIN public.users ON ((ai.created_by = users.user_id)))
             JOIN public.projects ON ((issues.project_id = projects.project_id)))
             LEFT JOIN public.issue_types previous_type ON ((ai.previous_type_id = previous_type.issue_type_id)))
             LEFT JOIN public.issue_types updated_type ON ((ai.updated_type_id = updated_type.issue_type_id)))
             LEFT JOIN public.issue_status previous_status ON ((ai.previous_status_id = previous_status.issue_status_id)))
             LEFT JOIN public.issue_status updated_status ON ((ai.updated_status_id = updated_status.issue_status_id)))
          WHERE (ai.audit_type = ANY (ARRAY['status_change'::public.audittype, 'comments'::public.audittype]))) audit;


ALTER TABLE public.audit_view OWNER TO postgres;

--
-- Name: issue_priority; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.issue_priority (
    issue_priority_id integer NOT NULL,
    issue_priority character varying
);


ALTER TABLE public.issue_priority OWNER TO postgres;

--
-- Name: issue_priority_issue_priority_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issue_priority_issue_priority_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issue_priority_issue_priority_id_seq OWNER TO postgres;

--
-- Name: issue_priority_issue_priority_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issue_priority_issue_priority_id_seq OWNED BY public.issue_priority.issue_priority_id;


--
-- Name: issue_status_issue_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issue_status_issue_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issue_status_issue_status_id_seq OWNER TO postgres;

--
-- Name: issue_status_issue_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issue_status_issue_status_id_seq OWNED BY public.issue_status.issue_status_id;


--
-- Name: issue_types_issue_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issue_types_issue_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issue_types_issue_type_id_seq OWNER TO postgres;

--
-- Name: issue_types_issue_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issue_types_issue_type_id_seq OWNED BY public.issue_types.issue_type_id;


--
-- Name: issues_issue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.issues_issue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.issues_issue_id_seq OWNER TO postgres;

--
-- Name: issues_issue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.issues_issue_id_seq OWNED BY public.issues.issue_id;


--
-- Name: milestones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.milestones (
    milestone_id integer NOT NULL,
    milestone character varying NOT NULL,
    milestone_date timestamp without time zone
);


ALTER TABLE public.milestones OWNER TO postgres;

--
-- Name: milestones_milestone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.milestones_milestone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.milestones_milestone_id_seq OWNER TO postgres;

--
-- Name: milestones_milestone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.milestones_milestone_id_seq OWNED BY public.milestones.milestone_id;


--
-- Name: modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modules (
    module_id integer NOT NULL,
    module_name character varying
);


ALTER TABLE public.modules OWNER TO postgres;

--
-- Name: modules_module_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.modules_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.modules_module_id_seq OWNER TO postgres;

--
-- Name: modules_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.modules_module_id_seq OWNED BY public.modules.module_id;


--
-- Name: organization_projects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_projects (
    organization_project_id integer NOT NULL,
    project_id integer NOT NULL,
    organization_id integer NOT NULL
);


ALTER TABLE public.organization_projects OWNER TO postgres;

--
-- Name: organization_projects_organization_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organization_projects_organization_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_projects_organization_project_id_seq OWNER TO postgres;

--
-- Name: organization_projects_organization_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organization_projects_organization_project_id_seq OWNED BY public.organization_projects.organization_project_id;


--
-- Name: organization_types; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_types (
    organization_type_id integer NOT NULL,
    type character varying,
    type_description character varying
);


ALTER TABLE public.organization_types OWNER TO postgres;

--
-- Name: organization_types_organization_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organization_types_organization_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organization_types_organization_type_id_seq OWNER TO postgres;

--
-- Name: organization_types_organization_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organization_types_organization_type_id_seq OWNED BY public.organization_types.organization_type_id;


--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    organization_id integer NOT NULL,
    organization_name character varying NOT NULL,
    organization_type_id integer NOT NULL,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Name: organizations_organization_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organizations_organization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.organizations_organization_id_seq OWNER TO postgres;

--
-- Name: organizations_organization_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organizations_organization_id_seq OWNED BY public.organizations.organization_id;


--
-- Name: project_milestones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_milestones (
    project_milestone_id integer NOT NULL,
    project_id integer NOT NULL,
    milestone_id integer NOT NULL
);


ALTER TABLE public.project_milestones OWNER TO postgres;

--
-- Name: project_milestones_project_milestone_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_milestones_project_milestone_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_milestones_project_milestone_id_seq OWNER TO postgres;

--
-- Name: project_milestones_project_milestone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_milestones_project_milestone_id_seq OWNED BY public.project_milestones.project_milestone_id;


--
-- Name: project_modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.project_modules (
    project_module_id integer NOT NULL,
    module_id integer NOT NULL,
    project_id integer NOT NULL
);


ALTER TABLE public.project_modules OWNER TO postgres;

--
-- Name: project_modules_project_module_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.project_modules_project_module_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.project_modules_project_module_id_seq OWNER TO postgres;

--
-- Name: project_modules_project_module_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.project_modules_project_module_id_seq OWNED BY public.project_modules.project_module_id;


--
-- Name: projects_project_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.projects_project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.projects_project_id_seq OWNER TO postgres;

--
-- Name: projects_project_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.projects_project_id_seq OWNED BY public.projects.project_id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: audit_issue audit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue ALTER COLUMN audit_id SET DEFAULT nextval('public.audit_issue_audit_id_seq'::regclass);


--
-- Name: issue_priority issue_priority_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_priority ALTER COLUMN issue_priority_id SET DEFAULT nextval('public.issue_priority_issue_priority_id_seq'::regclass);


--
-- Name: issue_status issue_status_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_status ALTER COLUMN issue_status_id SET DEFAULT nextval('public.issue_status_issue_status_id_seq'::regclass);


--
-- Name: issue_types issue_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_types ALTER COLUMN issue_type_id SET DEFAULT nextval('public.issue_types_issue_type_id_seq'::regclass);


--
-- Name: issues issue_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues ALTER COLUMN issue_id SET DEFAULT nextval('public.issues_issue_id_seq'::regclass);


--
-- Name: milestones milestone_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones ALTER COLUMN milestone_id SET DEFAULT nextval('public.milestones_milestone_id_seq'::regclass);


--
-- Name: modules module_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules ALTER COLUMN module_id SET DEFAULT nextval('public.modules_module_id_seq'::regclass);


--
-- Name: organization_projects organization_project_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_projects ALTER COLUMN organization_project_id SET DEFAULT nextval('public.organization_projects_organization_project_id_seq'::regclass);


--
-- Name: organization_types organization_type_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_types ALTER COLUMN organization_type_id SET DEFAULT nextval('public.organization_types_organization_type_id_seq'::regclass);


--
-- Name: organizations organization_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations ALTER COLUMN organization_id SET DEFAULT nextval('public.organizations_organization_id_seq'::regclass);


--
-- Name: project_milestones project_milestone_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_milestones ALTER COLUMN project_milestone_id SET DEFAULT nextval('public.project_milestones_project_milestone_id_seq'::regclass);


--
-- Name: project_modules project_module_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_modules ALTER COLUMN project_module_id SET DEFAULT nextval('public.project_modules_project_module_id_seq'::regclass);


--
-- Name: projects project_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects ALTER COLUMN project_id SET DEFAULT nextval('public.projects_project_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: audit_issue audit_issue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT audit_issue_pkey PRIMARY KEY (audit_id);


--
-- Name: issue_priority issue_priority_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_priority
    ADD CONSTRAINT issue_priority_pkey PRIMARY KEY (issue_priority_id);


--
-- Name: issue_priority issue_priority_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_priority
    ADD CONSTRAINT issue_priority_ukey UNIQUE (issue_priority);


--
-- Name: issue_status issue_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_status
    ADD CONSTRAINT issue_status_pkey PRIMARY KEY (issue_status_id);


--
-- Name: issue_status issue_status_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_status
    ADD CONSTRAINT issue_status_ukey UNIQUE (status);


--
-- Name: issue_types issue_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_types
    ADD CONSTRAINT issue_types_pkey PRIMARY KEY (issue_type_id);


--
-- Name: issue_types issue_types_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issue_types
    ADD CONSTRAINT issue_types_ukey UNIQUE (type);


--
-- Name: issues issues_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issues_pkey PRIMARY KEY (issue_id);


--
-- Name: milestones milestones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.milestones
    ADD CONSTRAINT milestones_pkey PRIMARY KEY (milestone_id);


--
-- Name: modules modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_pkey PRIMARY KEY (module_id);


--
-- Name: modules modules_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modules
    ADD CONSTRAINT modules_ukey UNIQUE (module_name);


--
-- Name: organization_projects organization_projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_projects
    ADD CONSTRAINT organization_projects_pkey PRIMARY KEY (organization_project_id);


--
-- Name: organization_types organization_types_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_types
    ADD CONSTRAINT organization_types_pkey PRIMARY KEY (organization_type_id);


--
-- Name: organization_types organization_types_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_types
    ADD CONSTRAINT organization_types_ukey UNIQUE (type);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (organization_id);


--
-- Name: organizations organizations_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_ukey UNIQUE (organization_name);


--
-- Name: project_milestones project_milestones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_milestones
    ADD CONSTRAINT project_milestones_pkey PRIMARY KEY (project_milestone_id);


--
-- Name: project_milestones project_milestones_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_milestones
    ADD CONSTRAINT project_milestones_ukey UNIQUE (project_id, milestone_id);


--
-- Name: project_modules project_modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_modules
    ADD CONSTRAINT project_modules_pkey PRIMARY KEY (project_module_id);


--
-- Name: project_modules project_modules_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_modules
    ADD CONSTRAINT project_modules_ukey UNIQUE (module_id, project_id);


--
-- Name: projects projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: projects projects_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.projects
    ADD CONSTRAINT projects_ukey UNIQUE (project_name);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_ukey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_ukey UNIQUE (email);


--
-- Name: audit_issue audit_issue_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT audit_issue_fkey FOREIGN KEY (issue_id) REFERENCES public.issues(issue_id);


--
-- Name: issues issue_assigned_to_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_assigned_to_fkey FOREIGN KEY (assigned_to) REFERENCES public.users(user_id);


--
-- Name: issues issue_created_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_created_user_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- Name: audit_issue issue_created_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT issue_created_user_fkey FOREIGN KEY (created_by) REFERENCES public.users(user_id);


--
-- Name: issues issue_milestone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_milestone_fkey FOREIGN KEY (milestone_id) REFERENCES public.project_milestones(project_milestone_id);


--
-- Name: issues issue_module_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_module_fkey FOREIGN KEY (module_id) REFERENCES public.project_modules(project_module_id);


--
-- Name: issues issue_priority_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_priority_fkey FOREIGN KEY (priority_id) REFERENCES public.issue_priority(issue_priority_id);


--
-- Name: issues issue_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_project_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: issues issue_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_status_fkey FOREIGN KEY (status_id) REFERENCES public.issue_status(issue_status_id);


--
-- Name: issues issue_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.issues
    ADD CONSTRAINT issue_type_fkey FOREIGN KEY (type_id) REFERENCES public.issue_types(issue_type_id);


--
-- Name: project_milestones milestone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_milestones
    ADD CONSTRAINT milestone_id_fkey FOREIGN KEY (milestone_id) REFERENCES public.milestones(milestone_id);


--
-- Name: project_modules module_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_modules
    ADD CONSTRAINT module_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: organization_projects organization_project_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_projects
    ADD CONSTRAINT organization_project_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(organization_id);


--
-- Name: organizations organizations_organization_types_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_organization_types_fkey FOREIGN KEY (organization_type_id) REFERENCES public.organization_types(organization_type_id);


--
-- Name: audit_issue previous_assignee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT previous_assignee_fkey FOREIGN KEY (previous_assignee_id) REFERENCES public.users(user_id);


--
-- Name: audit_issue previous_milestone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT previous_milestone_fkey FOREIGN KEY (previous_milestone_id) REFERENCES public.project_milestones(project_milestone_id);


--
-- Name: audit_issue previous_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT previous_status_fkey FOREIGN KEY (previous_status_id) REFERENCES public.issue_status(issue_status_id);


--
-- Name: audit_issue previous_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT previous_type_fkey FOREIGN KEY (previous_type_id) REFERENCES public.issue_types(issue_type_id);


--
-- Name: organization_projects project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_projects
    ADD CONSTRAINT project_id_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: project_milestones project_id_milestone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_milestones
    ADD CONSTRAINT project_id_milestone_fkey FOREIGN KEY (project_id) REFERENCES public.projects(project_id);


--
-- Name: project_modules project_module_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.project_modules
    ADD CONSTRAINT project_module_id_fkey FOREIGN KEY (module_id) REFERENCES public.modules(module_id);


--
-- Name: audit_issue updated_assignee_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT updated_assignee_fkey FOREIGN KEY (updated_assignee_id) REFERENCES public.users(user_id);


--
-- Name: audit_issue updated_milestone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT updated_milestone_fkey FOREIGN KEY (updated_milestone_id) REFERENCES public.project_milestones(project_milestone_id);


--
-- Name: audit_issue updated_status_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT updated_status_fkey FOREIGN KEY (updated_status_id) REFERENCES public.issue_status(issue_status_id);


--
-- Name: audit_issue updated_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_issue
    ADD CONSTRAINT updated_type_fkey FOREIGN KEY (updated_type_id) REFERENCES public.issue_types(issue_type_id);


--
-- Name: users users_organizations_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_organizations_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(organization_id);


--
-- PostgreSQL database dump complete
--

