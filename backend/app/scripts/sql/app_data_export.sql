--
-- PostgreSQL database dump
--

-- Dumped from database version 11.15 (Debian 11.15-1.pgdg90+1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg20.04+1)

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
SET session_replication_role to replica;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
8ecee885b906
\.


--
-- Data for Name: issue_priority; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_priority (issue_priority_id, issue_priority) FROM stdin;
1	High
2	Medium
3	Low
\.


--
-- Data for Name: issue_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_status (issue_status_id, status) FROM stdin;
1	Open
2	WIP
3	Completed
4	On-Hold
5	Closed
6	Re-Open
7	Duplicate
\.


--
-- Data for Name: issue_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_types (issue_type_id, type, type_description) FROM stdin;
1	New Requirement	New Requirement
2	Issue	Issue
3	Change Request	Change Request
4	Support Request	Support Request
\.


--
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modules (module_id, module_name) FROM stdin;
1	General
2	Dashboard
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (project_id, project_name, created_on) FROM stdin;
1	Track Application	2022-02-28 08:50:52.309978
\.


--
-- Data for Name: project_modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_modules (project_module_id, module_id, project_id) FROM stdin;
1	1	1
2	2	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, first_name, last_name, email, hashed_password, is_superuser, created_on, user_role) FROM stdin;
1	Admin	 	admin@trackapplication.in	$2b$12$ULrG.4MYOIPx1sreO/92NepaMO9Hc5B0m6prWyqciJvtSbnkwzR0u	t	2022-02-28 08:43:18.066461	lead
2	Madhan	Kumar	madhan@track.com	$2b$12$6EHbBGlDkgvuYpJiiOnuQe4k2t/U4acwigoxStQTXezp.kckr6Dfy	\N	2022-02-28 08:43:19.55162	lead
\.


--
-- Data for Name: issues; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issues (issue_id, issue_title, issue_description, project_id, type_id, status_id, priority_id, module_id, created_on, created_by, attachment_url, assigned_to) FROM stdin;
\.


--
-- Data for Name: audit_issue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_issue (audit_id, issue_id, previous_status_id, updated_status_id, previous_type_id, updated_type_id, comments, audit_type, attachment_url, created_on, created_by, previous_assignee_id, updated_assignee_id) FROM stdin;
\.


--
-- Name: audit_issue_audit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_issue_audit_id_seq', 1, false);


--
-- Name: issue_priority_issue_priority_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_priority_issue_priority_id_seq', 3, true);


--
-- Name: issue_status_issue_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_status_issue_status_id_seq', 7, true);


--
-- Name: issue_types_issue_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_types_issue_type_id_seq', 4, true);


--
-- Name: issues_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issues_issue_id_seq', 1, false);


--
-- Name: modules_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modules_module_id_seq', 2, true);


--
-- Name: project_modules_project_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_modules_project_module_id_seq', 2, true);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 2, true);


--
-- PostgreSQL database dump complete
--

