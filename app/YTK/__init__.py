from flask import Blueprint

YTK = Blueprint('YTK', __name__, static_folder='static', template_folder='templates')

from . import views, errors
from ..models import Permission

@YTK.app_context_processor
def inject_permissions():
    return dict(Pemission=Permission)
