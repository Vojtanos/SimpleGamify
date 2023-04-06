from flask import Blueprint
from services.seeder import Seeder
import click
from db import db

blp = Blueprint('custom-cli-interface', __name__, cli_group=None)

# flask [command = insert]
@blp.cli.command("insert")
def insert():
    Seeder.delete_all()
    Seeder.insert_config()
    db.session.commit()

@blp.cli.command("add")
@click.argument('config_path')
def insert(config_path):
    Seeder.add_config(config_path)
    Seeder.connect_users_to_new_config()
    db.session.commit()