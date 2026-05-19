import click
from comic_shelf.database import get_session, init_db
from comic_shelf.models import Publisher, Series, Issue, Collection, PullList, Wishlist
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
    
@cli.command()
@click.option('--series', prompt='Series name', help='The name of the series.')
@click.option('--issue-number', prompt='Issue number', type=int, help='The issue number.')
@click.option('--title', default=None, help='The title of the issue.')
@click.option('--release-date', default=None, help='The release date of the issue.')
def add_issue(series, issue_number, title, release_date):
    """Add a new issue to a series."""
    session = get_session()
    series_record = session.query(Series).filter_by(name=series).first()
    if not series_record:
        click.echo(f"Series '{series}' not found.")
        return
    issue = Issue(series=series_record, issue_number=issue_number, title=title, release_date=release_date)
    session.add(issue)
    try:
        session.commit()
        click.echo(f"Issue '{title}' (#{issue_number}) added successfully to series '{series}'.")
    except IntegrityError:
        session.rollback()
        click.echo(f"Issue #{issue_number} already exists in series '{series}'.")
        return
    
@cli.command()
@click.option('--issue-number', prompt='Issue number', type=int, help='The number of the issue to add to the collection.')
@click.option('--series', prompt='Series name', help='The name of the series for the issue.')
@click.option('--read', is_flag=True, help='Mark the issue as read.')
@click.option('--condition', default=None, help='The condition of the issue (e.g., Mint, Near Mint, Good).')
def add_to_collection(issue_number, series, read, condition):
    """Add an issue to the collection."""
    session = get_session()
    series_record = session.query(Series).filter_by(name=series).first()
    if not series_record:
        click.echo(f"Series '{series}' not found.")
        return
    issue_record = session.query(Issue).filter_by(series_id=series_record.id, issue_number=issue_number).first()
    if not issue_record:
        click.echo(f"Issue #{issue_number} not found in series '{series}'.")
        return
    collection_entry = Collection(issue=issue_record, read=read, condition=condition)
    session.add(collection_entry)
    try:
        session.commit()
        click.echo(f"Issue #{issue_number} added to collection successfully.")
    except IntegrityError:
        session.rollback()
        click.echo(f"Issue #{issue_number} is already in the collection.")
        return
    
if __name__ == '__main__':
    cli()