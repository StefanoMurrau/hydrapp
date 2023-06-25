from app import create_app

app = create_app()

if __name__ == "__main__":
    """
    The application is initialized with these arguments only when called directly from the run.py script. 
    In production it uses the parameters defined by the config.py, .env file and by the chosen web server (Gunicorn, Waitress, Apache or Nginx).
    """

    app.run(host=app.config.get("APP_HOST"), port=app.config.get("APP_PORT"), ssl_context=(app.config.get("APP_SSL_CONTEXT")[0], app.config.get("APP_SSL_CONTEXT")[1]))
    