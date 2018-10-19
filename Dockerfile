# Custom Dockerfile
FROM puckel/docker-airflow

# Install dependencies
# It's more efficient to do pip install here than adding a requirements.txt
USER root
RUN apt-get update -yqq \
    && usermod -a -G root airflow \
    && pip install docker

USER airflow