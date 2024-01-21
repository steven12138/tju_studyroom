FROM mariadb:11.1.3


ENV MYSQL_RANDOM_ROOT_PASSWORD=yes \
    MYSQL_DATABASE=studyroom \
    MYSQL_USER=studyroom \
    MYSQL_PASSWORD=123456

COPY ./init.sql /docker-entrypoint-initdb.d/