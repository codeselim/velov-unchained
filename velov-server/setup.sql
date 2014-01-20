CREATE role velovunchained LOGIN PASSWORD 'velovunchained' SUPERUSER;
CREATE DATABASE velovunchained;
GRANT ALL PRIVILEGES ON DATABASE velovunchained TO velovunchained;
commit;
\q