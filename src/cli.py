import click

from src.config import MIGRATIONS_ROOT
from src.database import db
from src.decorators import CollectionDecorator
from src.loader import import_method_by_module_str, load_migration_files


def migrate(direction: str):
    for file in load_migration_files(MIGRATIONS_ROOT):
        migration_fn = import_method_by_module_str(file, direction)
        operations = migration_fn(db)
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
