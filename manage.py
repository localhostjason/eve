from flask_script import Manager, Shell, Command
from flask_migrate import Migrate, MigrateCommand

from api import app, db
from api.admin import *
from api.frontEnd import *
import os
import time

from init_data import insert_admin

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


class ServerCommand(Command):
    @staticmethod
    def _get_pid():
        pid_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gunicorn.pid')
        try:
            with open(pid_file, 'r') as f:
                return int(f.read())
        except Exception as e:
            print(e)
            return None

    def get_status(self):
        pid = self._get_pid()
        if not pid:
            return False
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError as e:
            print(e)
            return False
        except Exception as e:
            print(e)
            return True


class Start(ServerCommand):
    """
    start gunicorn web server
    """

    def run(self):
        if self.get_status():
            return
        cmd = 'gunicorn -c gun.py manage:app --daemon'
        os.system(cmd)


class Stop(ServerCommand):
    """
    stop gunicorn web server
    """

    def run(self):
        pid = self._get_pid()
        if not pid:
            print('web server stopped')
            return
        try:
            os.kill(pid, 15)
        except ProcessLookupError as e:
            print('failed to kill pid:{},{}'.format(pid, str(e)))
        except PermissionError:
            pass
            print('no permission to kill pid {}'.format(pid))
        for i in range(3):
            if self.get_status():
                time.sleep(1)
        if self.get_status():
            print('web server failed to stop')


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('start', Start())
manager.add_command('stop', Stop())


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
