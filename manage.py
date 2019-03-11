from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from api import app, db
from api.admin import *

from init_data import insert_admin

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def update_db():
    from flask_migrate import upgrade, migrate

    migrate()
    upgrade()


@manager.command
def deploy():
    insert_admin()


if __name__ == '__main__':
    manager.run()
