 


FROM python:3.13-slim

RUN pip install pip --upgrade 
 
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt 
 
COPY . /app
EXPOSE 8000 
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]
 