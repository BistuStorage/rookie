dropdb mydb
createdb mydb
psql -d mydb -U postgres -f init.sql
