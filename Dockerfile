# Custom Dockerfile
FROM puckel/docker-airflow

# Install dependencies
# It's more efficient to do pip install here than adding a requirements.txt
USER airflow
USER root

COPY grant_access_to_airflow.sh /grant_access_to_airflow.sh

RUN apt-get update -yqq \
    && apt-get install wget -yqq \
    && pip install docker \
    && chmod 755 /grant_access_to_airflow.sh

ENTRYPOINT ["/grant_access_to_airflow.sh"]