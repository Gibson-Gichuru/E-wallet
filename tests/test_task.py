from tests import BaseTestConfig
from unittest import mock
from app.models import Task
from tests.settings import Settings


class TestTaskSchedule(BaseTestConfig):

    def setUp(self):
        super().setUp()

        self.user = Settings.create_user(active=True)

        # self.app.redis = mock.Mock()

        self.app.queue = mock.Mock()

        self.user.add(self.user)
    
    @mock.patch("app.models.failure", autospec=True)
    @mock.patch("app.models.success", autospec=True)
    @mock.patch("app.models.Task", autospec=True)
    def test_task_schedule(self,task_mock, success,failure):

        # queue_mock = mock.MagicMock(self.app.queue)

        target = mock.Mock(lambda a, b: a + b)

        description = "testing"

        job_mock = mock.Mock()

        job_mock.id.return_value = "some id"

        self.app.queue.enqueue.return_value = job_mock

        Task.schedule(
            owner=self.user,
            target_func=target,
            description=description,
            queue=self.app.queue,
            a=1,
            b=2
        )
       
        self.app.queue.enqueue.assert_called_with(
           target,
           description=description,
           on_success=success,
           on_failure=failure,
           a=1,
           b=2
       )

        task_mock.create_new.assert_called_with(
           task_id=job_mock.id,
           desc=description,
           initiator=self.user
       )
