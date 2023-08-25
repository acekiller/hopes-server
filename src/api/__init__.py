from .api import api_bp
from create_app import app

from . import user as _
from . import account as _
from . import forum as _

app.register_blueprint(api_bp)
