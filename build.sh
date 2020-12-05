docker-compose up --build -d
docker-compose exec web python manage.py collectstatic -c --no-input
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py add_users
docker-compose exec web python manage.py loaddata stores conversations
docker-compose restart
