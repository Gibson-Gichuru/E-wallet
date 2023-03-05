from app import db
from datetime import datetime
from app.message import send_sms
from app.job_callbacks import success, failure


class CrudOperations:

    def add(self, resource):

        db.session.add(resource)

        return db.session.commit()

    def update(self):

        return db.session.commit()
        
    def delete(self, resource):

        db.session.delete(resource)
        
        return db.session.commit()


class Actions:

    NOACTION = 0X00

    TRANSACT = 0X01 | 0X02

    STATEMENT = 0X04

    ACTIVATE = 0X08

    DEACTIVATE = 0X10

    BALANCECHECK = 0X02


class User(db.Model, CrudOperations):

    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)

    registation_date = db.Column(db.DateTime, default=datetime.utcnow)

    phonenumber = db.Column(db.String(50), nullable=False, unique=True)

    username = db.Column(db.String(50), nullable=False, unique=True)

    account = db.relationship("Account", uselist=False, back_populates="holder")

    tasks = db.relationship("Task", backref="owner", lazy="dynamic")

    def __init__(self, username, phonenumber) -> None:
        
        self.username = username

        self.phonenumber = phonenumber

        # create an account

        self.account  = Account()

    @staticmethod
    def account_statement(*args, **kwargs):

        records = kwargs.get("records")
        cumulative_debit = kwargs.get("cumulative_debit")
        cumulative_credit = kwargs.get("cumulative_credit")
        balance = kwargs.get("balance")
        recipient = kwargs.get("recipient")

        sms_format = Account.sms_statement_format(records=records)

        data = {
            "date":datetime.utcnow(),
            "records_str":sms_format,
            "cumulative_debit":cumulative_debit,
            "cumulative_credit":cumulative_credit,
            "balance":balance
        }

        send_sms(
            template="STATEMENT",
            recipient="+" + recipient,
            data=data
        )

    def __repr__(self) -> str:
        return "User: {}".format(self.username)


class Account(db.Model, CrudOperations):

    __tablename__ = "account"

    account_id = db.Column(db.Integer, primary_key=True)

    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'))

    balance = db.Column(db.Numeric(5,2), default=0.0)

    cumulative_debit = db.Column(db.Numeric(5,2), default=0.0)

    cumulative_credit = db.Column(db.Numeric(5,2), default=0.0)

    holder_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    holder = db.relationship("User", uselist=False, back_populates="account")

    payments = db.relationship("Payment", backref="account", lazy="dynamic")

    def __init__(self) -> None:
        
        default_status = Status.query.filter_by(
            default=True
        ).first()

        self.status = default_status

    def generate_statement(self):

        records = self.payments.all()

        return [
            dict(
                ref_no=record.transaction_id,
                amount=record.amount,
                date=datetime.strftime(
                    record.transaction_date,
                    "%Y-%m-%d %H:%M:%S"
                )
            )
            for record in records
        ]

    @staticmethod
    def sms_statement_format(records):

        record_str = ""

        for record in records:

            record_str += f"{record.get('ref_no')} {record.get('amount')} {record.get('date')}"

        return record_str

    def __repr__(self) -> str:
        
        return "Account Holder: {}".format(
            self.holder.username,
        )

    @staticmethod
    def update_balance(transaction_type, **kwargs):

        account = Account.query.filter_by(
            holder=kwargs.get("holder")
        ).first()

        if account is None:

            return

        if transaction_type.upper() == "CREDIT":

            account.balance += kwargs.get("amount")

            account.cumulative_credit += kwargs.get("amount")

        if transaction_type.upper() == "DEBIT" and account.balance > 0:

            account.balance -= kwargs.get("amount")

            account.cumulative_debit += kwargs.get("amount")

        account.update()

        return account

    @staticmethod
    def balance_notify(target, value, oldvalue, initiator):

        app = getattr(Account.balance_notify, "_current_app")

        with app.app_context():

            Task.schedule(
                owner=target.holder,
                description="Balance Notification",
                target_func=send_sms,
                queue=app.queue
            )

    @staticmethod
    def status_report_notify(target, value, oldvalue, initiator):

        Task.schedule(
            owner=target.holder,
            description="Account Status Change",
            target_func=send_sms
        )

    def can(self, action):

        return self.status is not None and (
            action & self.status.actions
        ) == action

    def deactivate(self):

        status = Status.query.filter_by(
            status_name="Deactivated"
        ).first()

        self.status = status

        self.update()


class Payment(db.Model, CrudOperations):

    __tablename__ = "payment"

    payment_id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.String(50), nullable=False, unique=True)

    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))

    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    amount = db.Column(db.Numeric(5,2), nullable=False)

    def __init__(self, transaction_id, account, date, amount) -> None:

        self.transaction_id = transaction_id

        self.account = account

        self.transaction_date = date

        self.amount = amount

    @staticmethod
    def register_to_account(mapper, conn, target):

        Task.schedule(
            owner=target.account.holder,
            description="Account Balance update",
            target_func=Account.update_balance,
            amount=target.amount,
            holder=target.account.holder
        )
        
    def __repr__(self) -> str:
        
        return "Recept: {}, Amount: {}, Date: {}".format(
            self.transaction_id,
            self.amount,
            self.transaction_date
        )


class Task(db.Model, CrudOperations):

    __tablename__ = "task"

    task_id = db.Column(db.String(50), primary_key=True)

    task_description = db.Column(db.String(50), nullable=False)

    completed = db.Column(db.Boolean, default=False)

    initiator = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __init__(self, task_id, desc, initiator) -> None:

        self.task_description = desc

        self.owner = initiator

        self.task_id = task_id

    @classmethod
    def create_new(cls, task_id, desc, initiator):

        new_task = cls(
            task_id=task_id,
            desc=desc,
            initiator=initiator
        )

        new_task.add(new_task)

        return new_task

    @staticmethod
    def schedule(
        owner,
        target_func=None,
        description=None,
        on_success=None,
        on_failure=None,
        queue=None,
        *args, **kwargs
    ):

        job = queue.enqueue(
            target_func,
            description=description,
            on_success=on_success if on_success else success,
            on_failure=on_failure if on_failure else failure,
            *args,
            **kwargs
        )

        Task.create_new(
            task_id=job.id,
            desc=description,
            initiator=owner
        )

    def __repr__(self) -> str:
        
        return "{}".format(
            self.task_description
        )


class Status(db.Model, CrudOperations):

    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)

    status_name = db.Column(db.String(50), nullable=False)

    actions = db.Column(db.Integer, nullable=False)

    default = db.Column(db.Boolean, default=False)

    account = db.relationship("Account", backref="status", lazy="dynamic")

    def __init__(self,name, actions, default=False) -> None:
        
        self.status_name = name

        self.actions = actions

        self.default = default

    def __repr__(self) -> str:
        
        return "{}".format(self.status_name)

    @staticmethod
    def register_actions():

        supported_actions = {
            "Active":(
                (
                 Actions.DEACTIVATE |
                 Actions.TRANSACT |
                 Actions.STATEMENT |
                 Actions.BALANCECHECK
                ),False
            ),
            "Suspended":(
                (
                    Actions.NOACTION
                ),False
            ),
            "Deactivated":(
                (Actions.ACTIVATE),True
            )
        }

        for action in supported_actions:

            action_exists = Status.query.filter_by(
                status_name=action
            ).first()

            if action_exists is None:

                new_status = Status(
                    name=action,
                    actions=supported_actions[action][0],
                    default=supported_actions[action][1]
                )

                new_status.add(new_status)
