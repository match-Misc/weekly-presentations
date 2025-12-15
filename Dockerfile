FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD sh -c "if [ ! -f db.sqlite3 ]; then python manage.py migrate; fi && python manage.py runserver 0.0.0.0:8000"