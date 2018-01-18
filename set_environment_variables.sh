#!/usr/bin/env bash
export AIRFLOW__CORE__AIRFLOW_HOME="/path/to/our/airflow/stuff"
export AIRFLOW__CORE__DAGS_FOLDER="${AIRFLOW__CORE__AIRFLOW_HOME}/dags"
export AIRFLOW__CORE__SQL_ALCHEMY_CONN="mysql://airflow:airflow@localhost:3306/airflow"
export AIRFLOW__CORE__LOAD_EXAMPLES="False"
export AIRFLOW__CORE__FERNET_KEY="some_secret_key"
export AIRFLOW__WEBSERVER__AUTH_BACKEND='airflow.contrib.auth.backends.password_auth'
export AIRFLOW__WEBSERVER__AUTHENTICATE='True'