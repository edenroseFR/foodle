from . import my_profile_bp
from flask import render_template, session
from . import utils
# from .utils import 
#     show_donor_details, 
#     get_user_data, 
#     has_org, get_role, 
#     parent_orgs, 
#     show_donor_details, 
#     get_total_foods,
#     get_total_beverages,
#     get_total_food_distributed,
#     get_total_bev_distributed,
#     get_collectors
from .forms import PersonalInformationForm

@my_profile_bp.route('/my_profile')
def index():
    form = PersonalInformationForm()
    user = session['email_address']
    role = utils.get_role(user)
    donor_details =  utils.show_donor_details(session["email_address"])
    user_data = utils.get_user_data(type='personal', email=user)
    address = utils.get_user_data(type='address', email=user)
    org = utils.has_org(user)
    org_info = ''
    parent_organizations=utils.parent_orgs()
    donor_details =  utils.show_donor_details(session["email_address"])
    donations_kls = utils.get_total_foods(session["email_address"])
    beverages_ltr = utils.get_total_beverages(session["email_address"])
    food_distributed = utils.get_total_food_distributed(session["email_address"])
    bev_distributed = utils.get_total_bev_distributed(session["email_address"])
    collectors = utils.get_collectors(session["email_address"])
    
    if org:
        org_info = utils.get_user_data(type='organization', email=user)
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
        parent_orgs=parent_organizations,
        donations_kls=donations_kls,
        beverages_ltr=beverages_ltr,
        food_distributed=food_distributed,
        bev_distributed=bev_distributed,
        collectors=collectors
    )
    