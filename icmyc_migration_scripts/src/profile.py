from mongoengine.fields import (
    StringField, IntField, BooleanField,DateTimeField,
    DictField, ListField, ObjectIdField
)
from mongoengine import Document
   

class Profile(Document):
    username = StringField(null=True)
    user_id = IntField(unique=True)
    email = StringField()
    password = StringField()
    full_name = StringField(required=False, max_length=255)
    mobile_number = StringField()
    otp = StringField()
    otp_sent_at = DateTimeField()
    mobile_number_verified = BooleanField()
    mobile_number_verified_at = DateTimeField()
    email_activation_token = StringField()
    email_activation_token_sent_at = DateTimeField()
    email_verified = BooleanField()
    email_verified_at = DateTimeField()
    mac_address = StringField()
    last_login_at = DateTimeField(null=True)
    last_login_ip = StringField()
    last_login_user_agent = StringField()
    last_login_channel = StringField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    otp_source = StringField()
    icmyc_user_id = IntField()
    sign_up_with = StringField(default='mobile_number')
    settings = DictField(default={"email_notifications_preferred": True, 
    "sms_notifications_preferred": True, 
    "push_notifications_preferred": True})
    sign_up_ip_address = StringField(null=True)
    sign_up_user_agent = StringField(null=True)
    has_at_least_one_social_account = BooleanField(default=False)
    social_accounts = ListField()
    channels = ListField()
    avatar = StringField(null=True)
    city_id = IntField()
    ward_id = IntField()

    meta = {'collection': 'profiles'}

    def __str__(self):
        return self.full_name
