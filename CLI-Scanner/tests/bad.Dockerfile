FROM python:latest

ENV AWS_SECRET_ACCESS_KEY=my-super-secret-key-123
ARG DB_PASSWORD=admin

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]