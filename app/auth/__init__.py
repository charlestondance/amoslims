from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views, errors
from ..models import Permission

@auth.app_context_processor
def inject_permissions():
    return dict(Pemission=Permission)
