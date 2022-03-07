from werkzeug.exceptions import SecurityError
from werkzeug.utils import redirect
from . import dashboard_bp
from flask import render_template, session, url_for, request, flash
from . import utils

@dashboard_bp.route('/donor/dashboard')
def donor_dashboard() -> str:
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        donations_kls = utils.get_total_foods(session["email_address"])
        beverages_ltr = utils.get_total_beverages(session["email_address"])
        food_distributed = utils.get_total_food_distributed(session["email_address"])
        bev_distributed = utils.get_total_bev_distributed(session["email_address"])
        collectors = utils.get_collectors(session["email_address"])
       

        return render_template('dashboard/donor_dashboard.html', donor = donor_details, 
            donations_kls = donations_kls,  beverages_ltr = beverages_ltr,  bev_distributed = bev_distributed,
            food_distributed=food_distributed, collectors = collectors) 
    else:
        return render_template('login/base.html')

@dashboard_bp.route('/collector/dashboard')
def collector_dashboard():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        food_distributed = utils.get_total_food_bev_distributed(session["email_address"])
        our_donors = utils.get_organization_donors(session["email_address"])
       
        return redirect(url_for('collectors_view.collectors_view'))
    else:
        return redirect(url_for('login.login'))


@dashboard_bp.route('/collector/dashboard/to distribute')
def to_distribute():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        collections = utils.get_items_for_distribution(session["email_address"])
        collections.reverse()
        return render_template('dashboard/org_to_distribute.html', donor = donor_details, collections=collections)

@dashboard_bp.route('/collector/dashboard/distributed', methods=['POST'])
def distribute():
    if 'email_address' in session:
        image_link1 = request.files['image_file1']
        image_link2 = request.files['image_file2']
        image_link3 = request.files['image_file3']
        img_storage = [image_link1, image_link2, image_link3]
        images = []
        for image in img_storage:
            if image.filename:
                img_link = utils.get_image_url(image)
                images.append(img_link)
        donation_id = request.args.get('id')
        utils.set_distributed_to_true(donation_id)
        utils.save_distribution_images(donation_id, images)
        utils.record_distribution(donation_id)
        return redirect(url_for('dashboard.to_distribute'))


@dashboard_bp.route('/collector/dashboard/to recieve')
def to_recieve():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        reserves = utils.get_items_to_collect(session["email_address"])
        reserves.reverse()
        return render_template('dashboard/org_to_collect.html', donor = donor_details, reserves=reserves)


@dashboard_bp.route('/collector/dashboard/recieved or collected')
def recieve_collect():
    if 'email_address' in session:
        donation_id = request.args.get('id')
        utils.set_collected_to_true(donation_id)
        return redirect(url_for('dashboard.to_recieve'))

@dashboard_bp.route('/collector/dashboard/completed collection')
def completed_collection():
    if 'email_address' in session:
        donor_details =  utils.show_donor_details(session["email_address"])
        completed = utils.get_completed_collections(session['email_address'])
        completed.reverse()
        return render_template('dashboard/org_completed.html', donor = donor_details, completed=completed)

        
@dashboard_bp.route('/collector/dashboard/cancel')
def collect_cancel():
    if 'email_address' in session:
        donation_id = request.args.get('id')
        utils.set_collected_to_false(donation_id)
        return redirect(url_for('dashboard.to_recieve'))
