FROM python:latest

ENV API_SECRET_KEY="super-secret-production-key-123"
ENV DB_PASSWORD="adminpassword"

WORKDIR /app

ADD requirements.txt .

RUN apt-get update && apt-get install -y curl vim netcat

RUN pip install -r requirements.txt

COPY . .

EXPOSE 22 8000

CMD ["python", "app.py"]
