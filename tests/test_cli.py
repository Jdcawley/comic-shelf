import pytest
from click.testing import CliRunner
from comic_shelf.cli import cli
from comic_shelf.database import init_db, engine
from comic_shelf.models import Base

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_add_publisher():
    runner = CliRunner()
    result = runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Test Publisher' added successfully." in result.output

def test_add_duplicate_publisher():
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    result = runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Test Publisher' already exists." in result.output

def test_add_series():
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    # Only invoke once and check that one result is successful
    result = runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Series 'Test Series' added successfully under publisher 'Test Publisher'." in result.output

def test_add_series_nonexistent_publisher():
    runner = CliRunner()
    result = runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Nonexistent Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Nonexistent Publisher' not found." in result.output

def test_add_issue():
    runner = CliRunner()
    # First, add a publisher and series to associate with the issue
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    result = runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    assert result.exit_code == 0
    assert "Issue 'Test Issue 1' (#1) added successfully to series 'Test Series'." in result.output

def test_add_duplicate_issue():
    runner = CliRunner()
    # First, add a publisher and series to associate with the issue
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    result = runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    assert result.exit_code == 0
    assert "Issue #1 already exists in series 'Test Series'." in result.output