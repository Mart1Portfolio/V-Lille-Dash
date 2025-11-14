FROM python:3.13

WORKDIR /app

COPY uv.lock .

RUN pip install uv 
RUN uv

COPY scrapy_function.py .
COPY scrapy_app.py .

ENV PORT=8080
CMD exec gunicorn -b :$PORT scrapy_app:app