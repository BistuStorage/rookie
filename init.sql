CREATE EXTENSION zhparser;
CREATE TEXT SEARCH CONFIGURATION chinesecfg (PARSER = zhparser);
ALTER TEXT SEARCH CONFIGURATION chinesecfg ADD MAPPING FOR n,v,a,i,e,l WITH simple;
create table dbm (name text primary key, fields text);
create table mdm (name text primary key, fields text);
create table users (id serial not null,username charracter varying(85) not null,password character varying(85) not null,privilege integer not null default 0,primary key(id));
create table invitation_code(code char(10) not null,privilege integer not null,primary key(code));
