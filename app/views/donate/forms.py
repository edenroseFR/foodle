from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms.fields import choices
from wtforms.fields.numeric import IntegerField
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
)
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed
from . import utils


class AddItemForm(FlaskForm):
    categories = utils.category_options()
    units = [(1, "kilos"), (2, "liters")]

    category = SelectField("Category", choices=categories, validators=[DataRequired()])
    quantity = IntegerField(
        "Quantity", validators=[DataRequired(), NumberRange(min=1, max=10)]
    )
    unit = SelectField("Unit", choices=units, validators=[DataRequired()])
    item_photo = FileField(
        "Upload Item Photo", validators=[FileAllowed(["jpg", "jpeg", "png", "gif"])]
    )
    add_item_btn = SubmitField("Add Item")
    edit_item_btn = SubmitField("Update Item")


class DonateForm(FlaskForm):
    street = StringField("Street *", validators=[DataRequired(), Length(min=5, max=50)])
    barangay = StringField(
        "Barangay *", validators=[DataRequired(), Length(min=5, max=50)]
    )
    city = StringField("City *", validators=[DataRequired(), Length(min=5, max=50)])
    transport_modes = utils.transport_mode_options()
    transport_mode = SelectField(
        "Mode of Transport", choices=transport_modes, validators=[DataRequired()]
    )
    donate_btn = SubmitField("Donate")
    donate_update_btn = SubmitField("Update Donation")
    update_donation_details = SubmitField("Update")
