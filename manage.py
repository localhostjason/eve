from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from api.domain import *
from api import app, db

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from flask_migrate import upgrade, migrate

    migrate()
    upgrade()


if __name__ == '__main__':
    manager.run()
