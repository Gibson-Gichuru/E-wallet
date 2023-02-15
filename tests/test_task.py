from tests import BaseTestConfig
from unittest import mock
from app.models import Task
from tests.settings import Settings


class TestTaskSchedule(BaseTestConfig):

    def setUp(self):
        super().setUp()

        self.user = Settings.create_user(active=True)

        self.user.add(self.user)

    @mock.patch("app.models.current_app.redis", autospec=True)
    @mock.patch("app.models.current_app.queue", autospec=True)
    @mock.patch("app.models_events.update_balance_success", autospec=True)
    def test_task_schedule(self,success_mock, queue_mock, redis_mock):

        target_func = mock.Mock(lambda a, b: a * b)

        description = "testing"

        Task.schedule(
            owner=self.user,
            description=description,
            target_func=target_func,
            on_success=success_mock,
            a=1,
            b=2
        )

        # assert that a job is scheduled

        queue_mock.enqueue.assert_called_with(
            target_func,
            description=description,
            on_success=success_mock,
            on_failure=None,
            a=1,
            b=2
        )
