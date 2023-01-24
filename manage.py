import os
import sys
from app import create_app

app = create_app(os.getenv("CONFIG") or "default")


@app.cli.command()
def test():

    import unittest

    tests = unittest.TestLoader().discover("tests")

    results = unittest.TextTestRunner(verbosity=2).run(tests)

    if not results.wasSuccessful():

        sys.exit()
