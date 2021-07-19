FROM python:3.7.3-slim-stretch

RUN apt-get -y update && apt-get -y install gcc
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn requests textract jsonlines PyPDF2 spacy==2.3.5 gunicorn python-multipart

RUN python -m spacy download en_core_web_sm

WORKDIR /app
COPY . .

# Make changes to the requirements/app here.
# This Dockerfile order allows Docker to cache the checkpoint layer
# and improve build times if making changes.

# COPY app.py /

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# ENTRYPOINT ["python3", "-X", "utf8", "app.py"]

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app:app
