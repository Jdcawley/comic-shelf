# comic-shelf
Personal comic book collection manager with pull list and wishlist tracking.

## About
Comic Shelf is a personal comic book collection manager built as a CLI application. 

The app solves a real problem with existing comic tracking apps — the inability to easily 
track comics you are on the fence about collecting on a week to week basis without fully 
committing to a pull list. Comic Shelf separates this into two distinct lists:

- **Collection** — comics you own
- **Pull List** — comics you are actively pulling from your local comic shop
- **Wishlist** — comics you are interested in but not yet committed to pulling

Built with Python, SQLAlchemy, and Click.

## Installation

1. Clone the repository
```bash
git clone https://github.com/Jdcawley/comic-shelf.git
cd comic-shelf
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Mac/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python -m comic_shelf.cli init
```

## Commands

### Publishers
| Command | Description |
|---------|-------------|
| `add-publisher --name "DC Comics"` | Add a new publisher |
| `list-publishers` | List all publishers |

### Series
| Command | Description |
|---------|-------------|
| `add-series --name "Batman" --publisher "DC Comics"` | Add a new series |
| `list-series` | List all series |

### Issues
| Command | Description |
|---------|-------------|
| `add-issue --series "Batman" --issue-number 1 --title "The Dark Knight"` | Add an issue to a series |

### Collection
| Command | Description |
|---------|-------------|
| `add-to-collection --series "Batman" --issue-number 1 --condition "Near Mint"` | Add an issue to your collection |
| `list-collection` | List your full collection |

### Pull List
| Command | Description |
|---------|-------------|
| `add-to-pull-list --series "Batman" --issue-number 1` | Add to pull list |
| `list-pull-list` | View your pull list |

### Wishlist
| Command | Description |
|---------|-------------|
| `add-to-wishlist --series "Batman" --issue-number 1 --notes "On the fence"` | Add to wishlist |
| `list-wishlist` | View your wishlist |


## Tech Stack 
- Python 3.13
- SQLAlchemy — ORM for database management
- SQLite — local database
- Click — CLI framework
- Pytest — testing

## Roadmap
- #1 Add sorting options to list-collection
- #2 Add display format options to list-collection
- #3 Add filter options to list-collection
- Phase 2: Comic Vine API integration
- Phase 3: Web UI
- Phase 4: AI-powered recommendations