import click
import sqlalchemy



@click.group()
def cli():
    pass

""""DB commands"""
@cli.command(short_help="Resetting the DB and creating a default user.")
@click.option(
    "--create-default-user",
    is_flag=True,
    help="Create a default user after resetting the database",
)
def reset_db(create_default_user):
    from database.db import reset_db

    reset_db()
    click.echo("Database reset")
    if create_default_user:
        from database.db import get_db
        from database.users import create_user

        db = get_db()
        create_user(db, "admin", "password")
        click.echo("Default user 'admin' created")
        db.close()


"""User commands"""
@cli.command(short_help="Import users from a CSV file.")
@click.argument("csv_file", type=click.Path(exists=True))
def import_users(csv_file):
    import csv
    from database.db import get_db
    from database.users import create_user
    import sqlalchemy.exc

    db = get_db()
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                create_user(db, row["username"], row["password"])
            except sqlalchemy.exc.IntegrityError:
                click.echo(f"User '{row['username']}' already exists, skipping")
                db.rollback()  # Rollback the transaction to continue with the next user
            else:
                click.echo(f"User '{row['username']}' imported from CSV")
    db.close()


""""Exercise commands"""
@cli.command(short_help="Add a new exercise to the database.")
@click.argument("name", type=str)
@click.argument("type", type=click.Choice(["WR", "RO", "CA", "FL"]))
def add_exercise(name, type):
    from database.db import get_db
    from database.exercises import insert_exercise
    from models import Exercise, ExerciseType

    db = get_db()
    exercise = Exercise(name=name, type=ExerciseType[type])
    insert_exercise(db, exercise)
    click.echo(f"Exercise '{name}' of type '{type}' added to the database")
    db.close()


@cli.command(short_help="Import exercises from a CSV file.")
@click.argument("csv_file", type=click.Path(exists=True))
def import_exercises(csv_file):
    import csv
    from database.db import get_db
    from database.exercises import insert_exercise
    from models import Exercise, ExerciseType

    db = get_db()
    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            exercise = Exercise(name=row["name"], type=ExerciseType[row["type"]])
            try:
                insert_exercise(db, exercise)
            except sqlalchemy.exc.IntegrityError:
                click.echo(f"Exercise '{row['name']}' of type '{row['type']}' already exists, skipping")
                db.rollback()  # Rollback the transaction to continue with the next exercise
            else:
                click.echo(f"Exercise '{row['name']}' of type '{row['type']}' imported from CSV")
    db.close()


if __name__ == "__main__":
    cli()
