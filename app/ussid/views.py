from flask.views import MethodView


class UssidCallback(MethodView):

    def __init__(self) -> None:
        super().__init__()

        self.response = ""

    def post(self):

        self.response  = "CON would you like \
             to regiser \n 1. Register Account \n 2. Cancel"

        return self.response
