FROM python:3.8.7-alpine3.12
WORKDIR /app
COPY ./src .
RUN pip install psycopg2
CMD ["python", "./par.py"]