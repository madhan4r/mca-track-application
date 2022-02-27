--
-- PostgreSQL database dump
--

-- Dumped from database version 11.15 (Debian 11.15-1.pgdg90+1)
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
SET session_replication_role to replica;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
64759630921e
\.


--
-- Data for Name: issue_priority; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_priority (issue_priority_id, issue_priority) FROM stdin;
\.


--
-- Data for Name: issue_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_status (issue_status_id, status) FROM stdin;
\.


--
-- Data for Name: issue_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issue_types (issue_type_id, type, type_description) FROM stdin;
\.


--
-- Data for Name: milestones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.milestones (milestone_id, milestone, milestone_date) FROM stdin;
\.


--
-- Data for Name: modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modules (module_id, module_name) FROM stdin;
\.


--
-- Data for Name: organization_types; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_types (organization_type_id, type, type_description) FROM stdin;
1	Service Provider	Service Provider
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizations (organization_id, organization_name, organization_type_id, created_on) FROM stdin;
1	Techno Consulting	1	2022-02-11 15:40:15.368336
\.


--
-- Data for Name: projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.projects (project_id, project_name, created_on) FROM stdin;
\.


--
-- Data for Name: project_milestones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_milestones (project_milestone_id, project_id, milestone_id) FROM stdin;
\.


--
-- Data for Name: project_modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.project_modules (project_module_id, module_id, project_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, organization_id, first_name, last_name, email, hashed_password, is_superuser, created_on, user_role) FROM stdin;
2	1	Senthil		senthil@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:24:35.609887	lead
3	1	Sri	Balaji	balaji@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:26:17.83051	lead
4	1	Gowtham	Ganesh	gowtham@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:33:01.618095	developer
5	1	Madhan	R	madhan@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:33:12.858116	developer
6	1	Kalingaraj	V	kalingaraj@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:43:15.638908	developer
7	1	Karkilan	Ravi	karkilan@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:43:36.179019	developer
8	1	Nova	Sangeeth	nova@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:43:50.458947	developer
9	1	Nithin	Barath	nithin@technoconsulting.in	$2b$12$IqOapWF.epNptg5A.HgpEedPU6ibGbHwOfFrkv2X06cB7O9Wvf5LS	f	2022-02-11 17:44:09.978478	developer
1	1	Admin		admin@technoconsulting.in	$2b$12$TDev4kooIxBnQpM6wSQ9GOt.Bz./DlI47Db.TjkKBq.WK96nEl9hO	t	2022-02-11 15:40:15.372373	lead
\.


--
-- Data for Name: issues; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.issues (issue_id, issue_title, issue_description, project_id, type_id, status_id, priority_id, milestone_id, module_id, gitlab_issue_id, created_on, created_by, attachment_url, assigned_to) FROM stdin;
\.


--
-- Data for Name: audit_issue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_issue (audit_id, issue_id, previous_status_id, updated_status_id, previous_type_id, updated_type_id, previous_milestone_id, updated_milestone_id, comments, audit_type, attachment_url, created_on, created_by, previous_assignee_id, updated_assignee_id) FROM stdin;
\.


--
-- Data for Name: organization_projects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_projects (organization_project_id, project_id, organization_id) FROM stdin;
\.


--
-- Name: audit_issue_audit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_issue_audit_id_seq', 1, false);


--
-- Name: issue_priority_issue_priority_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_priority_issue_priority_id_seq', 1, false);


--
-- Name: issue_status_issue_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_status_issue_status_id_seq', 1, false);


--
-- Name: issue_types_issue_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issue_types_issue_type_id_seq', 1, false);


--
-- Name: issues_issue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.issues_issue_id_seq', 1, false);


--
-- Name: milestones_milestone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.milestones_milestone_id_seq', 1, false);


--
-- Name: modules_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.modules_module_id_seq', 1, false);


--
-- Name: organization_projects_organization_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organization_projects_organization_project_id_seq', 1, false);


--
-- Name: organization_types_organization_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organization_types_organization_type_id_seq', 274, true);


--
-- Name: organizations_organization_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organizations_organization_id_seq', 1, true);


--
-- Name: project_milestones_project_milestone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_milestones_project_milestone_id_seq', 1, false);


--
-- Name: project_modules_project_module_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.project_modules_project_module_id_seq', 1, false);


--
-- Name: projects_project_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.projects_project_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 9, true);


--
-- PostgreSQL database dump complete
--

