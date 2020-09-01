from os import listdir
from os.path import isfile, join

import click

from src.database import db
from src.decorators import CollectionDecorator

MIGRATIONS_ROOT = "safe_migrations"


def load_migration_files(path):
    return [f for f in listdir(path) if isfile(join(path, f))]


def import_by_string(full_name):
    module_name, unit_name = full_name.rsplit(".", 1)
    return getattr(__import__(module_name, fromlist=[""]), unit_name)


def migrate(direction: str):
    for file in load_migration_files(MIGRATIONS_ROOT):
        file_path = join(MIGRATIONS_ROOT, file).replace("/", ".")
        function_path = file_path.replace("py", direction)
        up_func = import_by_string(function_path)
        operations = up_func(db)
        CollectionDecorator._migrate_pipeline(db, operations)


@click.group()
def cli():
    pass


@click.command()
def up():
    click.echo("Migrating UP")
    migrate("up")


@click.command()
def down():
    click.echo("Migrating DOWN")
    migrate("down")


@click.command()
def create():
    click.echo("Safe migrate CREATE")


@click.command()
def status():
    click.echo("Safe migrate STATUS")


cli.add_command(up)
cli.add_command(down)
cli.add_command(create)
cli.add_command(status)

if __name__ == "__main__":
    migrate("up")
