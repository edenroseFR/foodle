from werkzeug.utils import redirect
from . import donation_feed_bp
from flask import render_template, session, request, url_for, flash
from .utils import (
    get_collected_donations,
    get_distributed_donations,
    show_donor_details,
    get_posted_donations,
    delete_donation,
    get_reserved_donations,
    get_collected_donations,
    get_distributed_donations,
    cancel_reserved_donation,
    get_collected_donation_details,
    get_distributed_donation_details,
    get_distributed_donation_photo,
)
from app.views.donate.forms import DonateForm


@donation_feed_bp.route("/donor/donation feed/posted donations")
def posted_donations():
    donate_form = DonateForm()
    session_email = session["email_address"]
    donor_details = show_donor_details(session_email)
    posted_donations = get_posted_donations(session_email)

    return render_template(
        "donor_donation_tabs/posted_donations.html",
        donor=donor_details,
        donations=posted_donations,
        donate_form=donate_form,
    )


@donation_feed_bp.route("/donor/donation feed/reserved donations")
def reserved_donations():
    donate_form = DonateForm()
    session_email = session["email_address"]
    donor_details = show_donor_details(session_email)
    reserved_donations = get_reserved_donations(session_email)

    return render_template(
        "donor_donation_tabs/reserved_donations.html",
        donor=donor_details,
        donations=reserved_donations,
        donate_form=donate_form,
    )


@donation_feed_bp.route("/donor/donation feed/collected donations")
def collected_donations():
    donate_form = DonateForm()
    session_email = session["email_address"]
    donor_details = show_donor_details(session_email)
    donation_details = get_collected_donation_details(session_email)
    collected_donations = get_collected_donations(session_email)
    donations = zip(collected_donations.items(), donation_details.items())

    return render_template(
        "donor_donation_tabs/collected_donations.html",
        donor=donor_details,
        donations=donations,
        donate_form=donate_form,
        num_donation=len(collected_donations),
    )


@donation_feed_bp.route("/donor/donation feed/distributed donations")
def distributed_donations():
    donate_form = DonateForm()
    session_email = session["email_address"]
    donor_details = show_donor_details(session_email)

    donation_details = get_distributed_donation_details(session_email)
    distributed_donations = get_distributed_donations(session_email)
    distribution_photos = get_distributed_donation_photo(session_email)
    donations = zip(
        distributed_donations.items(),
        donation_details.items(),
        distribution_photos.items(),
    )

    return render_template(
        "donor_donation_tabs/distributed_donations.html",
        donor=donor_details,
        donations=donations,
        donate_form=donate_form,
        num_donation=len(distributed_donations),
    )


@donation_feed_bp.route("/donor/donation feed/delete donations")
def delete():
    donation_id = request.args.get("id")
    delete_donation(donation_id)

    flash("Post deleted", "danger")
    return redirect(url_for("donations.posted_donations"))


@donation_feed_bp.route("/donor/donation feed/edit donation")
def edit_donation():
    donation_id = request.args.get("id")
    delete_donation(donation_id)

    return redirect(url_for("donations.posted_donations"))


@donation_feed_bp.route("/donor/donation feed/cancel reserved donation")
def cancel_donation():
    donation_id = request.args.get("id")
    is_delete = bool(int(request.args.get("is_delete")))
    cancel_reserved_donation(donation_id, is_delete)

    flash("Donation cancelled", "danger")

    return redirect(url_for("donations.reserved_donations"))
