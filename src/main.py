"""
This is a cli entry point to the app meant for development purposes.
It is especially helpful for quickly validating CLI commands. Pass CLI options and args
to main.py as if passing to the tz application.
Usage:
    python main.py --help
"""

import typer

from timezones.app import app

__version__ = "0.0.1"

# Register commands
# app.command()(add.add)
# app.command()(command2.main)

@app.callback()
def callback():
    """callback for tz"""

@app.command()
def hello():
    typer.echo("hello world")

def version_callback(value: bool):
    if value:
        print(f"tz Version: {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
