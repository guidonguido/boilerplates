## FROM docker.io/library/postgres:latest
FROM docker.io/library/postgres:13-alpine

# Copy database dump.
COPY --chown=postgres:postgres      ./data/init.sql               /docker-entrypoint-initdb.d/init.sql
RUN chmod 750                       /docker-entrypoint-initdb.d/init.sql

# Add custom host-based authentication
# hba_file path in configuration must be set to /etc/postgresql/pg_hba.conf
COPY --chown=postgres:postgres      ./data/pg_hba.conf            /etc/postgresql/pg_hba.conf
RUN chmod 440                       /etc/postgresql/pg_hba.conf


# Add custom config
COPY --chown=postgres:postgres      ./data/postgresql.conf        /etc/postgresql/postgresql.conf
RUN chmod 440                       /etc/postgresql/postgresql.conf

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
# CMD ["postgres"]
