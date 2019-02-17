import click
from flask import Flask

from app import app

@click.group()
def cli():
    pass

@cli.command()
def run():
    app.run(host='0.0.0.0', port=8000, debug=True)


if __name__ == '__main__':
    cli()
