FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY backend /app/backend

COPY warptracker /app/warptracker

COPY manage.py /app/manage.py

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]