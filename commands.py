import click

from data.models import User, Bill, BillUser, BillItem

def create_admin():
    if User.get_or_none(User.is_superadmin) is not None:
        click.confirm('An admin user already exists ! Create another ?', abort=True)
    
    email = click.prompt('Email address', type=click.STRING)
    if User.get_by_email(email) is not None:
        raise click.UsageError('Email already taken')

    firstname = click.prompt('Firstname', type=click.STRING)
    surname = click.prompt('Lastname', type=click.STRING)
    password = click.prompt('Password', type=click.STRING, hide_input=True, confirmation_prompt=True)
    
    user = User.create(firstname=firstname, surname=surname, email=email, password=password, is_superadmin=True)

    if user is not None:
        click.echo('User added.')
    else:
        click.echo('An error occurred')

def create_database(db):
    db.database.create_tables([User, Bill, BillUser, BillItem])

def reset_database(db):
    db.database.drop_tables([User, Bill, BillUser, BillItem])
    create_database(db)

