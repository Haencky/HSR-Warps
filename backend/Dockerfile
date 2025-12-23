FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY hsr_pulls /app/hsr_pulls
COPY warps /app/warps
COPY manage.py /app/manage.py

EXPOSE 9001

ENTRYPOINT [ "python", "manage.py" ]

CMD ["runserver", "0.0.0.0:9001"]