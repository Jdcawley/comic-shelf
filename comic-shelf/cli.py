import click
from database import get_session, init_db
from models import Publisher, Series, Issue, Collection, PullList, Wishlist
from sqlalchemy.exc import IntegrityError

@click.group()
def cli():
    """Comic Shelf CLI - Manage your comic book collection, pull list, and wishlist."""
    pass

@cli.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Database initialized successfully.")

@cli.command()
@click.option('--name', prompt='Publisher name', help='The name of the publisher.')
def add_publisher(name):
    """Add a new publisher."""
    session = get_session()
    publisher = Publisher(name=name)
    session.add(publisher)
    try:
        session.commit()
        click.echo(f"Publisher '{name}' added successfully.")
    except IntegrityError:
        session.rollback()
        click.echo(f"Publisher '{name}' already exists.")
        return
    
@cli.command()
@click.option('--name', prompt='Series name', help='The name of the series.')
@click.option('--publisher', prompt='Publisher name', help='The name of the publisher for this series.')
def add_series(name, publisher):
    """Add a new series to a publisher."""
    session = get_session()
    publisher_record = session.query(Publisher).filter_by(name=publisher).first()
    if not publisher_record:
        click.echo(f"Publisher '{publisher}' not found.")
        return
    series = Series(name=name, publisher=publisher_record)
    session.add(series)
    try:
        session.commit()
        click.echo(f"Series '{name}' added successfully under publisher '{publisher}'.")
    except IntegrityError:
        session.rollback()
        click.echo(f"Series '{name}' already exists under publisher '{publisher}'.")
        return
    
if __name__ == '__main__':
    cli()