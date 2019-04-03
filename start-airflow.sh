#!/usr/bin/env bash
docker build --rm -t blinkenosa/docker-airflow .
docker-compose up -d