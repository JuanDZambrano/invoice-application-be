up:
		docker-compose up -d --build
		sleep 1
		docker-compose ps

down:
		docker-compose down

status:
		docker-compose ps

test: 
		docker-compose exec web python manage.py test 
