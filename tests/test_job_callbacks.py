from tests import BaseTestConfig
from unittest.mock import MagicMock
from unittest import mock
from app.job_callbacks import update_balance_success


class TestJobCallbacks(BaseTestConfig):

    @mock.patch("app.decorators.Task")
    def test_task_state_update(self, task_mock):

        task = job = result = connection = MagicMock()

        job.id.return_value = "test"

        update_balance_success(job, connection, result)

        task_mock.query.filter_by.first.return_value = task

        task.update.assert_called
