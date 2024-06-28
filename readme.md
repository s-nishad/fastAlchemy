
# Alembic Migrations with SQLAlchemy

This guide provides a step-by-step process for setting up Alembic migrations with SQLAlchemy in your project. Alembic is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

## Step 1: Install Alembic

First, you need to install Alembic. You can do this using pip:

```bash
pip install alembic
```

## Step 2: Initialize Alembic

Next, initialize Alembic in your project directory. This will create an `alembic` directory and an `alembic.ini` configuration file:

```bash
alembic init alembic
```

## Step 3: Configure `alembic.ini`

Open the `alembic.ini` file and set the `sqlalchemy.url` to point to your database. For example, if you're using SQLite:

```ini
sqlalchemy.url = sqlite:///database.db
```

## Step 4: Update `env.py`

In the `alembic/env.py` file, you need to import your `Base` object and set the `target_metadata` to your `Base.metadata`. This helps Alembic to understand your SQLAlchemy models:

```python
from myapp.models import Base  # Update this import to your actual Base
target_metadata = Base.metadata
```

## Step 5: Create a Migration Script

Generate a new migration script by running:

```bash
alembic revision --autogenerate -m "initial migrations"
```

This command will create a new migration script in the `alembic/versions` directory.

## Step 6: Apply Migrations

Finally, apply the migrations to your database by running:

```bash
alembic upgrade head
```

This will apply all the migrations up to the latest one, updating your database schema accordingly.

## Summary

You've now set up Alembic for your SQLAlchemy project, created an initial migration, and applied it to your database. Alembic makes it easy to manage database schema changes over time, which is crucial for maintaining the integrity of your application's data.

For more detailed information, refer to the [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/).

Happy coding!
