from unittest import mock
import functools
from app.models import User


class TaskTest:

    @staticmethod
    def task_wrapper(task_type):

        @mock.patch("app.ussid.views.User", autospec=True)
        @mock.patch("app.ussid.views.Messanger", autospec=True)
        @mock.patch("app.ussid.views.Task", autospec=True)
        @mock.patch("app.ussid.views.Mpesa", autospec=True)
        @mock.patch("app.ussid.views.success_notification", autospec=True)
        @mock.patch("app.ussid.views.failed_stk_push", autospec=True)
        @mock.patch("app.ussid.views.failed_notification", autospec=True)
        def decorator(
            func,
            failed_mock,
            failed_stk_mock,
            success_mock,
            mpesa_mock,
            task_mock,
            messanger_mock,
            user_mock
        ):

            @functools.wraps(func)
            def decorated_func(*args,**kwargs):

                user_obj_mock = mock.Mock()

                user_obj_mock.phonenumber.return_value = "some number"

                user_obj_mock.account.balance = 0

                user_mock.query.filter_by.return_value = user_obj_mock
                
                # preload the test

                func(*args, **kwargs)

                if task_type == "TOPUP":

                    task_mock.schedule.assert_called_with(
                        owner=user_obj_mock,
                        description="Topup Request",
                        target_func=mpesa_mock().stk_push,
                        on_success=success_mock,
                        on_failure=failed_stk_mock,
                        amount=100,
                        phonenumber=user_obj_mock.phonenumber
                    )

                if task_type == "STATEMENT":

                    task_mock.schedule.assert_called_with(
                        owner=user_obj_mock,
                        description="Account Statement",
                        target_func=User.generate_statement,
                        on_success=success_mock,
                        on_failure=failed_mock,
                        user=user_obj_mock
                    )

                if task_type == "BALANCE":

                    task_mock.schedule.assert_called_with(
                        owner=user_obj_mock,
                        description="Account Balance",
                        target_func=messanger_mock.send_sms,
                        on_success=success_mock,
                        on_failure=failed_mock,
                    )

                return

            return decorated_func

        return decorator
