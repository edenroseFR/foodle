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