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
    @mock.patch("app.models.current_app.queue", autospec=True)
    def test_task_schedule(self, queue_mock, task_mock):

        target_func = mock.Mock(lambda a, b: a * b)

        description="testing"

        Task.schedule(
            owner=self.user,
            description=description,
            target_func=target_func,
            a=1,
            b=2
        )

        # assert that a job is scheduled

        queue_mock.enqueue.assert_called_with(
            target_func,
            description=description,
            a=1,
            b=2
        )
