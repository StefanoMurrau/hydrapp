import logging.config
import os
import sys
from flask import Flask, render_template, current_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


def page_not_found(e) ->tuple:
    """
    If the user tries to access a page that doesn't exist, the function will render the 404.html
    template and return a 404 error code
    
    @param e The exception that was raised.
    @return A tuple of the rendered template and the HTTP status code.
    """

    display_name = current_app.config["PROJECT_NAME"]   
    return render_template('404.html', title = "Pagina non trovata", display_name=display_name), 404
    
def forbidden(e) ->tuple:
    """
    If the user tries to access a page that he/she is not allowed to, the user will be redirected to the
    403.html page
    
    @param e The exception that was raised.
    @return A tuple of the rendered template and the HTTP status code.
    """
    
    display_name = current_app.config["PROJECT_NAME"]   
    return render_template('403.html', title = "Accesso negato", display_name=display_name), 403

def internal_server_error(e) ->tuple:
    """
    If a page is impossible to render, the user will be redirected to the
    500.html page
   
    @param e The exception that was raised.
    @return A tuple of the rendered template and the HTTP status code.
    """
    
    display_name = current_app.config["PROJECT_NAME"]   
    return render_template('500.html', title = "Errore interno al server", display_name=display_name), 500

 
def create_app() ->Flask:
    """
    Create and configure the app
    
    @return The app object.
    """
    
    app = Flask(__name__, instance_relative_config=True)

    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    with app.app_context():
        try:
            app.config.from_object("config.DevelopmentConfig")
            logging.config.dictConfig( app.config["LOGGING_CONFIG"] )
        except Exception as e:
            sys.exit(f"ERROR. Cannot load config file: {repr(e)}")
       
        if not app.config.get("APPLICATION_ROOT") == "/":
            app.wsgi_app = DispatcherMiddleware(
                app.wsgi_app,{
                    app.config.get("APPLICATION_ROOT") : app.wsgi_app
                })
            
        app.register_error_handler(404, page_not_found)
        app.register_error_handler(403, forbidden)
        app.register_error_handler(500, internal_server_error)

        #Blueprints
        from app.main import main
        app.register_blueprint(main)
   
    return app
