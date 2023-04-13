from flask.cli import FlaskGroup

from src.app import app as app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()
