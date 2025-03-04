# Import all blueprint modules for registration in app/__init__.py
from app.routes.main import main
from app.routes.auth import auth
from app.routes.sailing import sailing
from app.routes.errors import errors