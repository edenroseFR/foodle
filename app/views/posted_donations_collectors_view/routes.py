from . import collectors_view_bp
from flask import render_template, redirect, url_for, request, session, flash
import app.models.donation as collect
import datetime as dt

@collectors_view_bp.route('/collector/view')
def collectors_view():
    city = collect.Donation().get_user_city(session['email_address'])
    donations = collect.Donation().get_collectables(city)
    donor_details = collect.Donation().get_donor_details(session['email_address'])
    return render_template('posted_donations_collectors_view/collectors_view.html', donations=donations, donor=donor_details)

@collectors_view_bp.route('/post/<donation_id>')
def collect_donation(donation_id):
    details = collect.Donation.get_verify_details(donation_id)
    collector_details = collect.Donation().get_donor_details(session['email_address'])
    return render_template('posted_donations_collectors_view/verify.html', collected=donation_id, details=details, collector=collector_details, donor=collector_details)

@collectors_view_bp.route('/post/verify/<donation_id>', methods=['POST'])
def confirm_donation(donation_id):
    if request.method == 'POST':
        datetime = dt.datetime.today()
        donation = collect.Donation().collect_verify(donation_id, session['email_address'], datetime)
    flash('Successfully reserved donation!', 'success')
    return redirect(url_for('collectors_view.collectors_view'))