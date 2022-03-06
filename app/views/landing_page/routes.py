from flask import render_template, request, session, redirect, url_for
from . import landing_bp
from ..login.forms import RegistrationForm
from ...models.donor_dashboard import Donor

@landing_bp.route('/')
def landing():
    reg_form = RegistrationForm()
    page_request = request.args.get('request_for')
    top_donors = Donor().get_donors_of_the_week()
    user_details = ''
    if 'email_address' in session:
        user_details = Donor().get_donor_details(session['email_address'])
        if page_request:
            return render_template('how_it_works/base.html', 
                scroll=page_request, 
                reg_form=reg_form,
                donor = user_details,
                top_donors = top_donors
            )
        else:
            return redirect(url_for('login.login'))
    else:
        if page_request:
                return render_template('how_it_works/base.html', 
                    scroll=page_request,
                    reg_form=reg_form,
                    donor = user_details,
                    top_donors = top_donors
                )
        else:
            return render_template('landing_page/base.html', 
                reg_form=reg_form,
                donor = user_details,
                top_donors = top_donors
            )