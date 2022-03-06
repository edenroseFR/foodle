from werkzeug.exceptions import SecurityError
from werkzeug.utils import redirect
from . import dashboard_bp
from flask import render_template, session, url_for, request, flash
from . import utils

@dashboard_bp.route('/collector/dashboard')
def collector_dashboard():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        food_distributed = utils.get_total_food_bev_distributed(session["email_address"])
        our_donors = utils.get_organization_donors(session["email_address"])
       
        return redirect(url_for("collectors_view.collectors_view"))
    else:
        return redirect(url_for('login.login'))

@dashboard_bp.route('/collector/dashboard/to recieve')
def to_recieve():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        reserves = utils.get_items_to_collect(session["email_address"])
        reserves.reverse()
        return render_template('dashboard/org_to_collect.html', donor = donor_details, reserves=reserves)

@dashboard_bp.route('/collector/dashboard/to distribute')
def to_distribute():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        collections = utils.get_items_for_distribution(session["email_address"])
        collections.reverse()
        return render_template('dashboard/org_to_distribute.html', donor = donor_details, collections=collections)

@dashboard_bp.route('/collector/dashboard/completed collection')
def completed_collection():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        completed = utils.get_completed_collections(session['email_address'])
        completed.reverse()
        return render_template('dashboard/org_completed.html', donor = donor_details, completed=completed)

@dashboard_bp.route('/collector/dashboard/recieved or collected')
def recieve_collect():
    if 'email_address' in session:
        donation_id = request.args.get('id')
        utils.set_collected_to_true(donation_id)
        return redirect(url_for('dashboard.to_recieve'))

@dashboard_bp.route('/collector/dashboard/cancel')
def collect_cancel():
    if 'email_address' in session:
        donation_id = request.args.get('id')
        utils.set_collected_to_false(donation_id)
        return redirect(url_for('dashboard.to_recieve'))