CREATE EXTENSION zhparser;
CREATE TEXT SEARCH CONFIGURATION chinesecfg (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION chinesecfg ADD MAPPING FOR n,v,a,i,e,l WITH simple;
CREATE TABLE DBM (name text primary key, fields text);
CREATE TABLE MDM (name text primary key, fields text);
