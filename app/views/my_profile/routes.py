from . import my_profile_bp
from flask import render_template, session
from .utils import show_donor_details, get_user_data, has_org, get_role, parent_orgs
from .forms import PersonalInformationForm

@my_profile_bp.route('/my_profile')
def index():
    form = PersonalInformationForm()
    user = session['email_address']
    role = get_role(user)
    donor_details =  show_donor_details(session["email_address"])
    user_data = get_user_data(type='personal', email=user)
    address = get_user_data(type='address', email=user)
    org = has_org(user)
    org_info = ''
    parent_organizations=parent_orgs()
    if org:
        org_info = get_user_data(type='organization', email=user)
    else:
        org_info = None
    if role == 'collector':
        role = 'Collector'
    else:
        role = 'Donor'
    return render_template(
        'my_profile/base.html', 
        form=form, 
        donor=donor_details, 
        org=org_info, 
        data=user_data, 
        address=address, 
        role=role, 
        user=user,
        parent_orgs=parent_organizations
    )
    