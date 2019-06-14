import os
import subprocess
import sys

import eventlet


#eventlet.monkey_patch()

COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='/app*')
    COV.start()

if os.path.exists('.env'):
    print('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


from app import create_app, db, socketio
from app.models import User
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Command, Server as _Server, Option


app = create_app()
#cli.register(app)


manager = Manager(app)
migrate = Migrate(app, db)

class Server(_Server):
    help = descriprion = 'Runs the Socket.IO web Server'

    def get_options(self):
        options = (
            Option('-h', '--host',
                   dest='host',
                   default=self.host),
            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),
            Option('-d', '--debug',
                   action='store_true',
                   dest='use_debugger',
                   help=('enable the Werkzeug debugger (DO NOT use in '
                         'production code)'),
                   default=self.use_debugger),

            Option('-D', '--no-debug',
                   action='store_false',
                   dest='use_debugger',
                   help='disable the Werkzeug debugger',
                   default=self.use_debugger),

            Option('-r', '--reload',
                   action='store_true',

                   dest='use_reloadr',
                   help=('monitor Python files for changes (not 100%% safe '
                         'for production use)'),
                   default=self.use_reloader),

            Option('-R', '--no-reload',
                   action='store_false',
                   dest='use_reloader',
                   help='do not monitor Python files for changes',
                   default=self.use_reloader),
        )
        return options

    def __call__(self, *args, **kwargs):
        socketio.run(app, host='127.0.0.1',
                     port=8000,
                     debug=True,
                     use_reloader=True,
                     **self.server_options
        )

manager.add_command("runserver", Server())


def make_shell_context():
    return dict(app=app, db=db, User=User)


manager.add_command("runserver", Server)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
