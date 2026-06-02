 


FROM python:3.13-slim

RUN pip install pip --upgrade 
 
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt 
# RUN pip install -U channels["daphne"]
COPY . /app
EXPOSE 8000 
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
# CMD ["daphne", "backend.routing:application","-b","0.0.0.0","-p","8000"]

# docker-compose exec backend sh -c "flake8 && pytest ."
# installed boto3 django-dotenv django-filter djangorestframework django-storages djangorestframework-simplejwt geocoder gunicorn whitenoise psycopg2-binary dj-database-urls