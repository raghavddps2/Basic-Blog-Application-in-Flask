# This is a classic blog application

## To use docker containers

- Install [docker-ce](https://docs.docker.com/install/)
- Install [docker-compose](https://docs.docker.com/compose/install/)
- You can see the current database structure in [sqldump.sql](sqldump.sql)
- The [sqldump.sql](sqldump.sql) file will be used to initialize the database as specified in [docker-compose.yml](docker-compose.yml)
- Run `docker-compose build` to build/rebuild containers 
- Run `docker-compose up` to start the containers
- Wait till the database is up, you will see message similar to the following after you run docker-compose up.  
 `db_1       | 2019-09-08T12:43:40.745433Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.17'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.`
- Changes you make to the application can be viewed in the browser
- Run `docker-compose down` to stop and remove  containers, networks, volumes, and images created
- To connect to the application, use url http://0.0.0.0:5000/
- To connect to adminer, use url http://localhost:8080/ and view/export the database