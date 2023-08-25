from .controllers import controller_bp as controller_bp
from create_app import app

from . import home as _
from . import abouts as _
from . import q_and_a as _
from . import account as _

app.register_blueprint(controller_bp)