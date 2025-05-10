FROM python:3.11

WORKDIR /app

COPY requeriments.txt requeriments.txt
RUN pip install -r requeriments.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
