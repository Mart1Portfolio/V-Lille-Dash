FROM python:3.13

WORKDIR /app

COPY requirements_scrapper.txt .

RUN pip install uv
RUN uv pip install -r requirements_scrapper.txt

COPY scrapy_function.py .
COPY scrapy_app.py .

ENV PORT=8080
CMD exec gunicorn -b :$PORT scrapy_app:app