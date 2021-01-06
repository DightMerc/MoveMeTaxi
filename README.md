MOVE ME
==============
JIRA (https://movemeuz.atlassian.net/jira/software/projects/MT/boards/1)

### What's included

 - Python 3.9.0
 - Django 3.1.2
 - PostgreSQL 13
 - Daphne 3.0.1 
 - Nginx 1.19.0
 
### Docker
 - Create `.env` file and configure this file
     ```
     $ cp .env.dist .env
     ```
 - Build a new image and run containers
     ```
     @dev:~$ docker-compose up -d --build
     @prod:~$ docker-compose -f docker-compose.prod.yml up -d --build
     ```
 - Flush and migrate database
     ```
     @dev:~$ docker-compose exec web python manage.py flush --no-input
     @dev:~$ docker-compose exec web python manage.py migrate
     @prod:~$ docker-compose -f docker-compose.prod.yml exec web python manage.py flush --no-input
     @prod:~$ docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
     ```
 - Checking for errors in logs
     ```
     @dev:~$ docker-compose logs -f
     @prod:~$ docker-compose -f docker-compose.prod.yml logs -f
     ```
 - Stop containers and bind volumes with the -v flag
     ```
     @dev:~$ docker-compose down -v
     @prod:~$ docker-compose -f docker-compose.prod.yml down -v
     ```