CREATE TABLE feed ( id INTEGER primary key,tick INTEGER, category VARCHAR(255),
 alliance1_id INTEGER, alliance2_id INTEGER, alliance3_id INTEGER, planet_id INTEGER, galaxy_id INTEGER, text VARCHAR(255));
CREATE SEQUENCE feed_id_seq 
 START WITH 1
 INCREMENT BY 1
 NO MINVALUE 
 NO MAXVALUE 
 CACHE 1;    
ALTER SEQUENCE feed_id_seq OWNED BY feed.id;
ALTER TABLE ONLY feed ALTER COLUMN id SET DEFAULT nextval('feed_id_seq'::regclass);

CREATE TABLE war (
    start_tick INTEGER,
    end_tick INTEGER,
    alliance1_id INTEGER,
    alliance2_id INTEGER);
ALTER TABLE ONLY war ADD CONSTRAINT war_pkey PRIMARY KEY (start_tick, alliance1_id, alliance2_id);
