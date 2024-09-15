FROM 842928376651.dkr.ecr.ap-south-1.amazonaws.com/python:3.8
ARG TOKEN
ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY
ENV PYTHONUBUFFERED=1
ENV AUDIENCE=7ce6b1dc-1cf0-4ea2-9461-e097180f2de7
ENV ALGORITHM=RS256
ENV ISSUER=https://login.microsoftonline.com/1bb287c4-8e33-476f-bf7b-a5e274c5b0e6/v2.0
ENV JWK_URL=https://login.microsoftonline.com/organizations/discovery/v2.0/keys
ENV postgres_host=postgresql.docsearch-qa.svc.cluster.local
ENV postgres_password=Q[Ml25?jRQw9gzE
ENV postgres_port=5432
ENV postgres_user=postgres
ENV PYTHONUBUFFERED=1
WORKDIR /code
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip3 install awscli
COPY . /code
RUN aws configure set aws_access_key_id $ACCESS_KEY_ID \
    && aws configure set aws_secret_access_key $SECRET_ACCESS_KEY \
    && aws configure set default.region ap-south-1 \
    && aws configure set default.output json
RUN chmod 777 script.sh

RUN apt-get update
RUN apt-get -y install cron
CMD ./script.sh
