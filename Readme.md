# This is a classic blog application

## To use docker containers

- Install [docker-ce](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- Install [docker-compose](https://docs.docker.com/compose/install/)
- Run `docker-compose build` to build/rebuild containers 
- Run `docker-compose up` to start the containers
- Wait till the database is up, you will see message similar to the following after you run docker-compose up.  
 `db_1       | 2019-09-08T12:43:40.745433Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.17'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.`
- Run `docker-compose down` to stop and remove  containers, networks, volumes, and images created
- To connect to the application, use url http://0.0.0.0:5000/
- To connect to adminer, use url http://localhost:8080/