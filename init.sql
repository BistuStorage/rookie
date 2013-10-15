CREATE EXTENSION zhparser;
CREATE TEXT SEARCH CONFIGURATION chinesecfg (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION chinesecfg ADD MAPPING FOR n,v,a,i,e,l WITH simple;
create table dbm (name text primary key, fields text);
