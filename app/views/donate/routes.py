from re import DOTALL
from flask.helpers import url_for
from werkzeug.datastructures import RequestCacheControl
from werkzeug.utils import redirect
from . import donate_bp
from flask import render_template, session, request, redirect, flash
from app.views.donate.forms import AddItemForm, DonateForm
from .utils import (
    show_donor_details,
    category_options,
    get_image_url,
    show_donation_items,
    add_donation,
    get_donation_details,
    update_donation,
)
import datetime as dt


added_items = []  # a list of items for to be posted donation
update_donation_added_items = []  # a list that stores the items of a posted donation


@donate_bp.route("/donor/donate", methods=["GET", "POST"])
def donate():
    item_form = AddItemForm()
    donate_form = DonateForm()
    donor_details = show_donor_details(session["email_address"])
    items = added_items
    category = category_options()

    return render_template(
        "donate/donate.html",
        donor=donor_details,
        item_form=item_form,
        donate_form=donate_form,
        added_items=items,
        num_items=len(added_items),
        category_options=category,
    )


@donate_bp.route("/donor/add-item", methods=["GET", "POST"])
def add_item():
    item_form = AddItemForm()

    if request.method == "POST":
        try:
            if len(added_items) != 5:
                category = int(item_form.category.data)
                quantity = item_form.quantity.data
                unit = item_form.unit.data
                item_photo = item_form.item_photo.data

                if item_photo != None:
                    item_photo_url = get_image_url(item_photo)
                    item = {
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "item_photo": item_photo_url,
                    }
                    added_items.append(item)
                else:
                    item = {
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "item_photo": "https://res.cloudinary.com/deh9vgcga/image/upload/v1638773718/brand_jpm78c.png",
                    }
                    added_items.append(item)
        except:
            flash("An error has occured. Please try again!", "danger")

    return redirect(url_for("donate.donate"))


@donate_bp.route("/donor/delete-item", methods=["GET", "POST"])
def delete_item():
    if request.method == "POST":
        index = int(request.form["temp_item_id"]) - 1
        added_items.pop(index)

    return redirect(url_for("donate.donate"))


@donate_bp.route("/donor/edit-item", methods=["GET", "POST"])
def edit_item():
    try:
        item_form = AddItemForm()
        category = int(item_form.category.data)
        quantity = item_form.quantity.data
        unit = item_form.unit.data
        item_photo = item_form.item_photo.data

        temp_item_id = int(request.form["temp_item_id"]) - 1

        if item_photo == None:
            added_items[temp_item_id] = {
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "item_photo": added_items[temp_item_id]["item_photo"],
            }
        else:
            item_photo_url = get_image_url(item_photo)
            added_items[temp_item_id] = {
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "item_photo": item_photo_url,
            }

    except:
        flash("An error has occured. Please try again!", "danger")
    return redirect(url_for("donate.donate"))


@donate_bp.route("/donor/donate-item", methods=["GET", "POST"])
def donate_donation():
    if request.method == "POST":
        donate_form = DonateForm()
        datetime = dt.datetime.today()
        street = donate_form.street.data
        barangay = donate_form.barangay.data
        city = donate_form.city.data
        transport_mode = donate_form.transport_mode.data

        add_donation(
            session["email_address"],
            added_items,
            datetime,
            transport_mode,
            street,
            barangay,
            city,
        )

    added_items.clear()
    flash("Posted", "success")
    return redirect(url_for("donations.posted_donations"))


@donate_bp.route("/donor/donate/get-donation-items", methods=["GET", "POST"])
def get_donation_items():
    update_donation_added_items.clear()
    id = request.args.get("id")
    session["donation_id"] = id
    items = show_donation_items(session["donation_id"])
    for i in items:  # i[c,q,u,url]
        item = {"category": i[0], "quantity": i[1], "unit": i[2], "item_photo": i[3]}
        update_donation_added_items.append(item)

    return redirect(url_for("donate.edit_posted_donation"))


# loads the items in the database on the donate page
@donate_bp.route("/donor/donate/edit-donation", methods=["GET", "POST"])
def edit_posted_donation():
    item_form = AddItemForm()
    donate_form = DonateForm()
    category = category_options()
    donor_details = show_donor_details(session["email_address"])

    donation_details = get_donation_details(session["donation_id"])

    return render_template(
        "donate/edit_donation.html",
        donor=donor_details,
        item_form=item_form,
        donate_form=donate_form,
        added_items=update_donation_added_items,
        num_items=len(update_donation_added_items),
        donation_details=donation_details,
        category_options=category,
    )


@donate_bp.route("/donor/donation/add-item", methods=["GET", "POST"])
def update_donation_add_item():
    item_form = AddItemForm()

    if request.method == "POST":
        try:
            if len(added_items) != 5:
                category = int(item_form.category.data)
                quantity = item_form.quantity.data
                unit = item_form.unit.data
                item_photo = item_form.item_photo.data

                if item_photo != None:
                    item_photo_url = get_image_url(item_photo)
                    item = {
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "item_photo": item_photo_url,
                    }
                    update_donation_added_items.append(item)
                else:
                    item = {
                        "category": category,
                        "quantity": quantity,
                        "unit": unit,
                        "item_photo": "https://res.cloudinary.com/deh9vgcga/image/upload/v1638773718/brand_jpm78c.png",
                    }
                    update_donation_added_items.append(item)
        except:
            flash("An error has occured. Please try again!", "danger")

    return redirect(url_for("donate.edit_posted_donation"))


@donate_bp.route("/donor/donation/delete-item", methods=["GET", "POST"])
def update_donation_delete_item():
    if request.method == "POST":
        index = int(request.form["temp_item_id"]) - 1
        update_donation_added_items.pop(index)

    return redirect(url_for("donate.edit_posted_donation"))


@donate_bp.route("/donor/donation/edit-item", methods=["GET", "POST"])
def update_donation_edit_item():
    try:
        item_form = AddItemForm()
        category = int(request.form.get("category"))
        quantity = item_form.quantity.data
        unit = request.form.get("unit")
        item_photo = item_form.item_photo.data
        temp_item_id = int(request.form["temp_item_id"]) - 1

        if item_photo == None:
            update_donation_added_items[temp_item_id] = {
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "item_photo": update_donation_added_items[temp_item_id]["item_photo"],
            }
        else:
            item_photo_url = get_image_url(item_photo)
            update_donation_added_items[temp_item_id] = {
                "category": category,
                "quantity": quantity,
                "unit": unit,
                "item_photo": item_photo_url,
            }

    except:
        flash("An error has occured. Please try again!", "danger")

    return redirect(url_for("donate.edit_posted_donation"))


@donate_bp.route("/donor/update-donation", methods=["GET", "POST"])
def update_donation():
    if request.method == "POST":
        donate_form = DonateForm()
        datetime = dt.datetime.today()
        street = donate_form.street.data
        barangay = donate_form.barangay.data
        city = donate_form.city.data
        transport_mode = donate_form.transport_mode.data
        number_of_items = len(update_donation_added_items)
        update_donation(
            session["donation_id"],
            update_donation_added_items,
            datetime,
            transport_mode,
            number_of_items,
            street,
            barangay,
            city,
        )

    update_donation_added_items.clear()
    flash("Updated!", "success")
    return redirect(url_for("donations.posted_donations"))
