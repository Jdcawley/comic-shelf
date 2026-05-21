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
    
@cli.command()
def list_publishers():
    """List all publishers."""
    session = get_session()
    publishers = session.query(Publisher).all()
    if not publishers:
        click.echo("No publishers found.")
        return
    click.echo("Publishers:")
    click.echo("-----------")
    for publisher in publishers:
        click.echo(f"{publisher.name}")

@cli.command()
def list_series():
    """List all series."""
    session = get_session()
    series_list = session.query(Series).all()
    if not series_list:
        click.echo("No series found.")
        return
    click.echo("Series:")
    click.echo("-------")
    for series in series_list:
        click.echo(f"{series.name}, Publisher: {series.publisher.name}")

# TODO: Add sorting options (recently added, alphabetical)
# TODO: Add display format options (grouped by publisher/series, flat list)
# TODO: Allow user to filter by read/unread, condition
@cli.command()
def list_collection():
    """List all issues in the collection."""
    session = get_session()
    collection_entries = session.query(Collection).all()
    if not collection_entries:
        click.echo("No issues in the collection.")
        return
    click.echo("Collection:")
    click.echo("-----------")
    for entry in collection_entries:
        issue = entry.issue
        series = issue.series
        publisher = series.publisher
        if publisher.name != current_publisher:
            current_publisher = publisher.name
            click.echo(f"\n{publisher.name}")
        if series.name != current_series:
            current_series = series.name
            click.echo(f"  {series.name}")
        title = f" - {issue.title}" if issue.title else ""
        read = "Yes" if entry.read else "No"
        condition = entry.condition or "N/A"
        click.echo(f"    #{issue.issue_number}{title} | Read: {read} | Condition: {condition}")

@cli.command()
@click.option('--series', prompt='Series name', help='The name of the series to add to the pull list.')
@click.option('--issue-number', type=int, default=None, help='The issue number to add to the pull list (optional).')
def add_to_pull_list(series, issue_number):
    """Add a series to the pull list."""
    session = get_session()
    series_record = session.query(Series).filter_by(name=series).first()
    if not series_record:
        click.echo(f"Series '{series}' not found.")
        return
    # Check first before adding to avoid unnecessary database entries
    existing_entry = session.query(PullList).filter_by(series_id=series_record.id, issue_number=issue_number, active=True).first()
    if existing_entry:
        if issue_number:
            click.echo(f"Issue '#{issue_number}' of series '{series}' is already in the pull list.")
        else:
            click.echo(f"'{series}' is already in the pull list.")
        return
    pull_list_entry = PullList(series=series_record, issue_number=issue_number)
    session.add(pull_list_entry)
    session.commit()
    if issue_number:
        click.echo(f"Issue '#{issue_number}' of series '{series}' added to pull list successfully.")
    else:
        click.echo(f"Series '{series}' added to pull list successfully.")

@cli.command()
@click.option('--series', prompt='Series name', help='The name of the series to add to the wishlist.')
@click.option('--issue-number', type=int, default=None, help='The issue number to add to the wishlist (optional).')
@click.option('--notes', default=None, help='Additional notes for the wishlist entry.')
def add_to_wishlist(series, issue_number, notes):
    """Add a series to the wishlist."""
    session = get_session()
    series_record = session.query(Series).filter_by(name=series).first()
    if not series_record:
        click.echo(f"Series '{series}' not found.")
        return
    # Check first before adding to avoid unnecessary database entries
    existing_entry = session.query(Wishlist).filter_by(series_id=series_record.id, issue_number=issue_number, active=True).first()
    if existing_entry:
        if issue_number:
            click.echo(f"Issue '#{issue_number}' of series '{series}' is already in the wishlist.")
        else:
            click.echo(f"'{series}' is already in the wishlist.")
        return
    wishlist_entry = Wishlist(series=series_record, issue_number=issue_number, notes=notes)
    session.add(wishlist_entry)
    session.commit()
    if issue_number:
        click.echo(f"Issue '#{issue_number}' of series '{series}' added to wishlist successfully.")
    else:
        click.echo(f"Series '{series}' added to wishlist successfully.")
    
    
if __name__ == '__main__':
    cli()