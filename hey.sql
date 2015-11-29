--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: activities_act; Type: TABLE; Schema: public; Owner: windson; Tablespace: 
--

ALTER TABLE activities_act OWNER TO windson;

--
-- Name: activities_act_id_seq; Type: SEQUENCE; Schema: public; Owner: windson
--

CREATE SEQUENCE activities_act_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE activities_act_id_seq OWNER TO windson;

--
-- Name: activities_act_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: windson
--

ALTER SEQUENCE activities_act_id_seq OWNED BY common_act.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: windson
--

ALTER TABLE ONLY activities_act ALTER COLUMN id SET DEFAULT nextval('common_act_id_seq'::regclass);


--
-- Data for Name: activities_act; Type: TABLE DATA; Schema: public; Owner: windson
--

COPY activities_act (id, act_title, act_content, act_thumb_url, act_ident, act_type, act_licence, act_star, act_status, act_url, act_delete, act_create_time, user_id) FROM stdin;
1	车厘子的明信片	为了纪念车厘子，我们把车厘子的图片都做成明信片，然后免费分发给陌生人，让他们写下对最爱的人说的话，再帮他们寄出去。	http://7xokch.com1.z0.glb.clouddn.com/uni_cherry678.png?imageView2/0/w/320/format/jpeg	100000	0	4	0	0	/act/Windson/车厘子的明信片	0	2014-04-01 00:00:00+08	22
8	罗赛塔计划	罗塞塔号（Rosetta）是欧洲空间局组织的机器人空间探测器计划，研究67P/楚留莫夫－格拉希门克彗星。[4][5]2004年3月2日在圭亚那太空中心发射，10年8个多月后进入彗星轨道，随后其所带菲莱登陆器则于2014年11月12日在彗星上着陆。	http://7xokch.com1.z0.glb.clouddn.com/mars678.png?imageView2/0/w/320/format/jpeg	100006	1	5	0	0	0	0	2014-11-01 00:00:00+08	22
9	南极冰川	目前“南地极”位于南极洲内，并插有标记。但由于大陆漂移，在地球的历史上其实大多数时间南极洲都在距离南极很远的地方；而且，每隔一段时间，地理学家都要修正南极的位置。上一次修正南极位置的时间在2000年。	http://7xokch.com1.z0.glb.clouddn.com/ice678.png?imageView2/0/w/320/format/jpeg	100007	1	5	0	0	0	0	2014-12-01 00:00:00+08	22
10	Pacific Ocean	The Pacific Ocean is the largest of the Earth's oceanic divisions. It extends from the Arctic Ocean 	http://7xokch.com1.z0.glb.clouddn.com/otherice678.png?imageView2/0/w/320/format/jpeg	100008	1	5	0	0	0	0	2015-01-01 00:00:00+08	22
2	亲吻陌生人	爱不分地域，种族与性别，上传你的照片，会随机吻上一位陌生人。和TA聊聊.爱不分地域，种族与性别，上传你的照片，会随机吻上一位陌生人。和TA聊聊.爱不分地域，种族与性别，上传你的照片，会随机吻上一位陌生人。和TA聊聊	http://7xokch.com1.z0.glb.clouddn.com/uni_kiss678.png?imageView2/0/w/320/format/jpeg	100001	2	4	0	0	/act/Windson/亲吻陌生人	0	2014-05-01 00:00:00+08	22
3	说出你的爱	不要吝惜你的爱。	http://7xokch.com1.z0.glb.clouddn.com/uni_say678.png?imageView2/0/w/320/format/jpeg	100002	2	4	0	0	/act/Windson/说出你的爱	0	2014-06-01 00:00:00+08	22
4	广州大学的互相帮助	一些简单的生活问题，可以在此发表。	http://7xokch.com1.z0.glb.clouddn.com/uni_help678.png?imageView2/0/w/320/format/jpeg	100003	2	4	0	0	/act/Windson/广州大学的互相帮助	0	2014-07-01 00:00:00+08	22
5	世界各地的童工	全球现在约有1亿6800万名儿童做劳工，其中半数人的工作存在危险性。现今，全球仍有10%儿童因被迫工作而失学。	http://7xokch.com1.z0.glb.clouddn.com/uni_child678.png?imageView2/0/w/320/format/jpeg	100004	0	4	0	0	/act/Windson/世界各地的童工	0	2014-08-01 00:00:00+08	22
6	一瞬之美	无数的前期准备，以及对抗癌症以及化疗的决心，只为这一秒。	http://7xokch.com1.z0.glb.clouddn.com/uni_asecond678.png?imageView2/0/w/320/format/jpeg	100005	0	4	0	0	/act/Windson/一瞬之美	0	2014-09-01 00:00:00+08	22
\.


--
-- Name: activities_act_id_seq; Type: SEQUENCE SET; Schema: public; Owner: windson
--

SELECT pg_catalog.setval('activities_act_id_seq', 10, true);


--
-- Name: activities_act_act_ident_524b890500bc2616_uniq; Type: CONSTRAINT; Schema: public; Owner: windson; Tablespace: 
--

ALTER TABLE ONLY activities_act
    ADD CONSTRAINT activities_act_act_ident_524b890500bc2616_uniq UNIQUE (act_ident);


--
-- Name: activities_act_pkey; Type: CONSTRAINT; Schema: public; Owner: windson; Tablespace: 
--

ALTER TABLE ONLY activities_act
    ADD CONSTRAINT activities_act_pkey PRIMARY KEY (id);


--
-- Name: activities_act_e8701ad4; Type: INDEX; Schema: public; Owner: windson; Tablespace: 
--

CREATE INDEX activities_act_e8701ad4 ON common_act USING btree (user_id);


--
-- Name: activities_act_user_id_2d30b042e6f68733_fk_common_user_id; Type: FK CONSTRAINT; Schema: public; Owner: windson
--

ALTER TABLE ONLY activities_act
    ADD CONSTRAINT activities_act_user_id_2d30b042e6f68733_fk_common_user_id FOREIGN KEY (user_id) REFERENCES common_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

