FROM python:3.12

COPY . /app
WORKDIR /app
RUN pip install -r /app/requirements.txt

CMD ["python", "-m", "bootstrap"]
