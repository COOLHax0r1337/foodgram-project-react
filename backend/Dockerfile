FROM python:3.9-slim
WORKDIR /code
COPY requirements.txt .
RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install -r requirements.txt
COPY foodgram/ .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8001" ]