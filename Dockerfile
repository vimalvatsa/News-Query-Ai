FROM python:3.8-slim
ENV PYTHONUBUFFERED=1
WORKDIR /code
COPY requirements.txt ./

RUN pip3 install -r requirements.txt 

# Install Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

COPY . /app
RUN apt-get update
CMD ./script.sh
