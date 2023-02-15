from tests import BaseTestConfig
from unittest import mock
from app.models import Task
from tests.settings import Settings


class TestTaskSchedule(BaseTestConfig):

    def setUp(self):
        super().setUp()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)
    
    @mock.patch("app.models.Task", autospec=True)
    @mock.patch("app.models.current_app.queue")
    def test_task_schedule(self, queue_mock, task_mock):

        target = on_failure = mock.Mock(lambda a, b: a + b)

        description = "testing"

        job_mock = mock.Mock()

        job_mock.id.return_value = "some id"

        queue_mock.enqueue.return_value = job_mock

        Task.schedule(
            owner=self.user,
            target_func=target,
            description=description,
            on_failure=on_failure,
            a=1,
            b=2
        )
       
        queue_mock.enqueue.assert_called_with(
           target,
           description=description,
           on_success=None,
           on_failure=on_failure,
           a=1,
           b=2
       )

        task_mock.create_new.assert_called_with(
           task_id=job_mock.id,
           desc=description,
           initiator=self.user
       )
