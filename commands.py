import click
import uuid

from email_validator import validate_email, EmailNotValidError

from data.models import User, MODELS

def create_admin():
    if len(User.get_superadmins()) > 0:
        click.confirm('An admin user already exists ! Create another ?', abort=True)
    
    email = click.prompt('Email address', type=click.STRING)
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        raise click.UsageError('Email is not valid')
            
    if User.get_by_email(email):
        raise click.UsageError('Email already taken')

    firstname = click.prompt('Firstname', type=click.STRING)
    surname = click.prompt('Lastname', type=click.STRING)
    password = click.prompt('Password', type=click.STRING, hide_input=True, confirmation_prompt=True)
    
    user = User.create(uuid=uuid.uuid4(), firstname=firstname, surname=surname, email=email, password=password, is_superadmin=True)

    if user:
        click.echo('User added')
    else:
        click.echo('An error occurred')

def create_database(db):
    db.database.create_tables(MODELS)

def reset_database(db):
    db.database.drop_tables(MODELS)
    create_database(db)

