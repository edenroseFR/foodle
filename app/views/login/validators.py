from wtforms.validators import ValidationError
from email import message
from .utils import check_email_registration
from .utils import check_contact_registration
from .utils import check_org_registration



def unique_email(form, field):
    message = 'Email already registered.'
    if check_email_registration(field.data) == True:
        raise ValidationError(message)

class UniqueEmail:

    def __init__(
        self,
        message=None,
        granular_message=False,
        check_deliverability=False,
        allow_smtputf8=True,
        allow_empty_local=False,
    ):
        self.message = message
        self.granular_message = granular_message
        self.check_deliverability = check_deliverability
        self.allow_smtputf8 = allow_smtputf8
        self.allow_empty_local = allow_empty_local
    
    
    def __call__(self, form, field):
        if check_email_registration(field.data) == True:
            message = 'Email already registered.'
            raise ValidationError(message)


def unique_org(form, field):
    message = 'Organization already registered'
    if check_org_registration(field.data) == True:
        raise ValidationError(message)


def unique_number(form, field):
    message = 'Phone Number already registered'
    if check_contact_registration(field.data) == True:
        raise ValidationError(message)