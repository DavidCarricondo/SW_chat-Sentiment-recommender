from src.app import app
from src.config import PORT
import src.controllers.user


if __name__ == '__main__':
    app.run('0.0.0.0',PORT, debug=True)