import pytest
from click.testing import CliRunner
from comic_shelf.cli import cli
from comic_shelf.database import init_db, engine
from comic_shelf.models import Base

# Fixture that runs before and after every test
# Creates a fresh database before each test and drops all tables after
# autouse=True means it runs automatically without needing to be called explicitly
@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

# --- Publisher Tests ---

def test_add_publisher():
    """Test that a publisher can be added successfully."""
    runner = CliRunner()
    result = runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Test Publisher' added successfully." in result.output

def test_add_duplicate_publisher():
    """Test that adding a duplicate publisher returns an error message."""
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    result = runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Test Publisher' already exists." in result.output

# --- Series Tests ---

def test_add_series():
    """Test that a series can be added successfully under an existing publisher."""
    runner = CliRunner()
    # Publisher must exist before a series can be added
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    result = runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    assert result.exit_code == 0
    assert "Series 'Test Series' added successfully under publisher 'Test Publisher'." in result.output

def test_add_series_nonexistent_publisher():
    """Test that adding a series under a nonexistent publisher returns an error message."""
    runner = CliRunner()
    result = runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Nonexistent Publisher'])
    assert result.exit_code == 0
    assert "Publisher 'Nonexistent Publisher' not found." in result.output

# --- Issue Tests ---

def test_add_issue():
    """Test that an issue can be added successfully to an existing series."""
    runner = CliRunner()
    # Publisher and series must exist before an issue can be added
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    result = runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    assert result.exit_code == 0
    assert "Issue 'Test Issue 1' (#1) added successfully to series 'Test Series'." in result.output

def test_add_duplicate_issue():
    """Test that adding a duplicate issue number to the same series returns an error message."""
    runner = CliRunner()
    # Publisher and series must exist before an issue can be added
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    result = runner.invoke(cli, ['add-issue', '--series', 'Test Series', '--issue-number', '1', '--title', 'Test Issue 1'])
    assert result.exit_code == 0
    assert "Issue #1 already exists in series 'Test Series'." in result.output

# --- Pull List Tests ---

def test_add_to_pull_list():
    """Test that a specific issue can be added to the pull list successfully."""
    runner = CliRunner()
    # Publisher and series must exist before adding to pull list
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    result = runner.invoke(cli, ['add-to-pull-list', '--series', 'Test Series', '--issue-number', '1'])
    assert result.exit_code == 0
    assert "Issue '#1' of series 'Test Series' added to pull list successfully." in result.output

def test_add_duplicate_pull_list_entry():
    """Test that adding a duplicate entry to the pull list returns an error message."""
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    runner.invoke(cli, ['add-to-pull-list', '--series', 'Test Series', '--issue-number', '1'])
    result = runner.invoke(cli, ['add-to-pull-list', '--series', 'Test Series', '--issue-number', '1'])
    assert result.exit_code == 0
    assert "Issue '#1' of series 'Test Series' is already in the pull list." in result.output

def test_add_to_pull_list_nonexistent_series():
    """Test that adding to pull list with a nonexistent series returns an error message."""
    runner = CliRunner()
    result = runner.invoke(cli, ['add-to-pull-list', '--series', 'Nonexistent Series', '--issue-number', '1'])
    assert result.exit_code == 0
    assert "Series 'Nonexistent Series' not found." in result.output

def test_list_pull_list():
    """Test that the pull list displays added entries correctly."""
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    runner.invoke(cli, ['add-to-pull-list', '--series', 'Test Series', '--issue-number', '1'])
    result = runner.invoke(cli, ['list-pull-list'])
    assert result.exit_code == 0
    assert "Pull List:" in result.output
    assert "Test Series #1" in result.output

# --- Wishlist Tests ---

def test_add_to_wishlist():
    """Test that a specific issue can be added to the wishlist successfully."""
    runner = CliRunner()
    # Publisher and series must exist before adding to wishlist
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    result = runner.invoke(cli, ['add-to-wishlist', '--series', 'Test Series', '--issue-number', '1', '--notes', 'Must read!'])
    assert result.exit_code == 0
    assert "Issue '#1' of series 'Test Series' added to wishlist successfully." in result.output

def test_add_duplicate_wishlist_entry():
    """Test that adding a duplicate entry to the wishlist returns an error message."""
    runner = CliRunner()
    runner.invoke(cli, ['add-publisher', '--name', 'Test Publisher'])
    runner.invoke(cli, ['add-series', '--name', 'Test Series', '--publisher', 'Test Publisher'])
    runner.invoke(cli, ['add-to-wishlist', '--series', 'Test Series', '--issue-number', '1', '--notes', 'Must read!'])
    result = runner.invoke(cli, ['add-to-wishlist', '--series', 'Test Series', '--issue-number', '1', '--notes', 'Must read!'])
    assert result.exit_code == 0
    assert "Issue '#1' of series 'Test Series' is already in the wishlist." in result.output