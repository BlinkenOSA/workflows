import logging

from datetime import datetime
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from airflow.operators.sensors import BaseSensorOperator

log = logging.getLogger(__name__)

class OSA_AV_Plugins(AirflowPlugin):
	name = "OSA AV Digitization workflow plugin"
	operators = []
