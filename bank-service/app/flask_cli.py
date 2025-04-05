import os
import dotenv
import click

from flask.cli import with_appcontext

from app.extensions import db


dotenv.load_dotenv()


def create_roles():
    from app.models.role import Role

    roles = [os.getenv('DEFAULT_ROLE'), 'admin']

    click.echo('Creating roles')
    for role in roles:
        if not Role.query.filter_by(name=role).first():
            db.session.add(Role(name=role))
        else:
            click.echo('Roles already exists')
            return
    db.session.commit()


def create_admin():
    """Create a new admin user"""
    from app.models.user import User
    from app.api.schemas.user import UserSchema

    admin_info = {
        'email': os.getenv('ADMIN_EMAIL'),
        'password': os.getenv('ADMIN_PASS'),
        'roles': ['admin'],
    }

    data = UserSchema().load(admin_info)

    click.echo('Creating admin user')
    if (User.query.filter_by(email=data.get('email', None)).first()):
        click.echo('Admin already exists')
        return

    admin = User(**data)

    db.session.add(admin)
    db.session.commit()


@click.command('init')
@with_appcontext
def init():
    create_roles()
    create_admin()
