-- Create users.
CREATE USER keycloak WITH PASSWORD 'DBuserPassword';

-- Create databases.
CREATE DATABASE keycloak;

-- Grant users privileges on their own databases.
GRANT ALL PRIVILEGES ON DATABASE keycloak TO keycloak;
