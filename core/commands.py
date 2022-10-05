import click

from core import app, db
from core.models import User

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()

    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def admin():
    """Add administrator account."""
    user = User(name='admin')
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()
    click.echo('Added administrator account.')

@app.cli.command()
def restart():
    """Restart the server."""
    db.drop_all()
    db.create_all()
    click.echo('Restarted database.')

    user = User(name='admin')
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()
    click.echo('Added administrator account.')
