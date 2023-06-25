from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired
from wtforms.widgets.core import html_params


class CustomSelect:
    """
    Renders a select field allowing custom attributes for options.
    Expects the field to be an iterable object of Option fields.
    The render function accepts a dictionary of option ids ("{field_id}-{option_index}")
    which contain a dictionary of attributes to be passed to the option.

    Example:
    form.customselect(option_attr={"customselect-0": {"disabled": ""} })
    """

    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, option_attr=None, **kwargs):
        if option_attr is None:
            option_attr = {}
        kwargs.setdefault("id", field.id)
        if self.multiple:
            kwargs["multiple"] = True
        if "required" not in kwargs and "required" in getattr(field, "flags", []):
            kwargs["required"] = True
        html = ["<select %s>" % html_params(name=field.name, **kwargs)]
        for option in field:
            attr = option_attr.get(option.id, {})
            html.append(option(**attr))
        html.append("</select>")
        return Markup("".join(html))


#########################################
# NAV FORM                              #
######################################### 
class nav_form(FlaskForm):
    """
    This is a FlaskForm class with four SelectFields for selecting data type, run reference, run
    configuration, and time.
    """
    
    data_type = SelectField(
        "Data Type", 
        choices=[("", "Type")], 
        validators=[DataRequired()], 
        name="data-type", 
        widget=CustomSelect(), 
        default="",
        render_kw={"class":"form-control", "data-target":"run-reference"}
    )
    
    run_reference = SelectField(
        "Run Reference", 
        choices=[("", "Run Reference")], 
        validators=[DataRequired()], 
        name="run-reference", 
        widget=CustomSelect(),
        default="", 
        render_kw={"class":"form-control", "data-target":"run-configuration", "disabled": "disabled"}
    )
    
    run_configuration = SelectField(
        "Run Configuration", 
        choices=[("", "Run Configuration")], 
        validators=[DataRequired()], 
        name="run-configuration", 
        widget=CustomSelect(),
        default="", 
        render_kw={"class":"form-control", "disabled": "disabled"}
    )
    
    time = StringField(
        "Time", 
        validators=[DataRequired()], 
        name="time", 
        render_kw={"class":"form-control", "disabled": "disabled", "placeholder": "DD/MM/YYYY"}
    )
