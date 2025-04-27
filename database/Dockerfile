FROM postgres:17.4-bookworm


ENV POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres

COPY ./init/init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432
