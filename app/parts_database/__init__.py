from flask import Blueprint

parts_database = Blueprint('parts_database', __name__, static_folder='static', template_folder='templates')

from . import views, errors
from ..models import Permission

@parts_database.app_context_processor
def inject_permissions():
    return dict(Pemission=Permission)
