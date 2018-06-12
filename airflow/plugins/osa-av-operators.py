import logging

from datetime import datetime
from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults
from airflow.operators.sensors import BaseSensorOperator

log = logging.getLogger(__name__)


class CreateDirectoryStructureOperator(BaseOperator):

	@apply_defaults
	def __init__(self, param, *args, **kwargs):
		self.operator_param = param
		super(CreateDirectoryStructureOperator, self).__init__(*args, **kwargs)

	def execute(self, context):
		log.info("CreateDirectoryStructureOperator class execute method invoked")
		log.info("parameter was: %s", self.operator_param)
		task_instance = context["task_instance"]


class OSA_AV_Plugins(AirflowPlugin):
	name = "OSA AV Digitization workflow plugin"
	operators = [CreateDirectoryStructureOperator]
