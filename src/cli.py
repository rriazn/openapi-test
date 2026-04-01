import click



@click.group()
def cli():
    pass


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


if __name__ == "__main__":
    cli()
