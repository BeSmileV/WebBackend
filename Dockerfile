FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000
#CMD ["gunicorn", "web_backend.wsgi:application", "-w", "2", "-b", ":8000","--reload"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
