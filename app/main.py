from flask import Blueprint, abort, render_template, request, jsonify, current_app, Markup, flash, url_for, redirect
from jinja2 import TemplateNotFound
from app.form import nav_form
from os import path
from app.functions import get_data_from_csv, get_data_types, get_images_basedirs, list_images
from app.form import nav_form


main = Blueprint('main', __name__)


BASEDIR = path.abspath(path.dirname(__file__))


#########################################
# HOMEPAGE                              #                                              
#########################################
@main.route('/')
def home():
    """
    The `home()` function defines a route for the home page, renders a dashboard template with a
    navigation form, and returns it with the title "Cruscotto" and a navigation form object as a
    parameter.
    
    @return The function `home()` returns the rendered template "dashboard.html" with the title
    "Cruscotto" and a navigation form object `form` as a parameter.
    """

    try: 
        display_name = current_app.config["PROJECT_NAME"]
        
        form = nav_form()
        data_types = get_data_types()
        
        if not data_types[0]:
            msg = Markup(f"Errore.</br><i>{data_types[1]}</i>")
            flash(msg, 'danger')
            abort(500)
        else:
            for d in data_types[1]:
                form.data_type.choices.append(d)
        return render_template("dashboard.html", title="Cruscotto", form=form, display_name=display_name)
    except TemplateNotFound:
        abort(404)


#########################################
# UPDATE RUN REFERENCE                  #                                              
#########################################
@main.route('/update-run-reference', methods=['GET','POST'])

def update_run_reference():
    """
    This function updates a run reference with data from a CSV file and returns the target and data if
    successful, or displays an error message if not.
    
    @return If the request method is POST and the data is successfully retrieved from the CSV file, a
    JSON object containing the target and the retrieved data is returned. If there is an error, a flash
    message with the error details is displayed and the function redirects to the home page. If the
    request method is not POST, the function also redirects to the home page.
    """

    if request.method == "POST":
        try:
            target = request.json["target"]
            csv = request.json["csv"]
            
            data = get_data_from_csv(csv, target)
            if not data[0]:
                msg = Markup(f"Errore.</br><i>{data[1]}</i>")
                flash(msg, 'danger')
                return jsonify(False)
            else:
                return jsonify([target, data[1]])
        except Exception as e:
            msg = Markup(f"Errore.</br><i>{repr(e)}</i>")
            flash(msg, 'danger')
            return jsonify(False)
  
        
#########################################
# UPDATE RUN CONFIGURATION              #                                              
#########################################
@main.route('/update-run-configuration', methods=['GET','POST'])
def update_run_configuration():
    """
    The function updates a run reference with data from a CSV file and returns the target and data if
    successful, or displays an error message if not.
    
    @return If the request method is POST and the data is successfully retrieved from the CSV file, a
    JSON object containing the target and the retrieved data is returned. If there is an error, a flash
    message with the error details is displayed and the function redirects to the home page. If the
    request method is not POST, the function also redirects to the home page.
    """

    if request.method == "POST":
        try:
            target = request.json["target"]
            run_reference = request.json["run_reference"]
            csv = request.json["csv"]

            data = get_data_from_csv(csv, target, run_reference)
            if not data[0]:
                msg = Markup(f"Errore.</br><i>{data[1]}</i>")
                flash(msg, 'danger')
                return jsonify(False)
            else:
                return jsonify([target, data[1]])
        except Exception as e:
            msg = Markup(f"Errore.</br><i>{repr(e)}</i>")
            flash(msg, 'danger')
            return jsonify(False)
        
 
#########################################
# GET IMAGES                            #                                              
#########################################
@main.route('/get-images', methods=['GET','POST'])
def get_images():
    """
    """

    if request.method == "POST":
        try:
            run_configuration = request.json["run-configuration"]
            run_reference = request.json["run_reference"]
            csv = request.json["csv"]
            date = request.json["date"]
            formated_date =  date[6:10] + date[3:5] + date[0:2]

            data = get_images_basedirs(csv, run_reference, run_configuration, formated_date)
            if not data[0]:
                msg = Markup(f"Errore.</br><i>{data[1]}</i>")
                flash(msg, 'danger')
                return jsonify(False)
            else:
                imgs = list_images(data[1])
                
                return jsonify(imgs)
        except Exception as e:
            msg = Markup(f"Errore.</br><i>{repr(e)}</i>")
            flash(msg, 'danger')
            return jsonify(False)     