# av-preservation-workflow
Blinken OSA AV Preservation workflows implemented with Airflow (https://airflow.apache.org)

## Install

1. `pip install -r requirements.txt`
2. Confiugre `AIRFLOW__CORE__AIRFLOW_HOME` environmental variable
3. Create database according to `AIRFLOW__CORE__SQL_ALCHEMY_CONN` or setup a different one. (For development purpose you can skip this configuration option and use the default sqlite one.)
4. Run: `airflow initdb`
5. Create user according to the manual: https://airflow.apache.org/security.html#password
6. Fire up airflow: `airflow webserver -p 8080`
