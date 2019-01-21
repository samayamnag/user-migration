from mongoengine import connect
from dotenv import load_dotenv
from utils import getenv, validate_mobile_number, now
from models import IcmycUser, User
from base_sqlalchemy import Base, ICMYCSession, SwachhataSession
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from profile import Profile
from channel import Channel
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = BASE_DIR + '/.env'

load_dotenv(dotenv_path=env_path, verbose=True)

# Swachhata Mongo connection
connect(
    getenv('SWACHHATA_MONGO_DB_NAME'),
    host=getenv("SWACHHATA_MONGO_DB_HOST"),
    port=int(getenv("SWACHHATA_MONGO_DB_PORT")),
    username=getenv('SWACHHATA_MONGO_DB_USERNAME'),
    password=getenv("SWACHHATA_MONGO_DB_PASSWORD")
    )

# Get icmyc users
def fetch_icmyc_users(from_id, to_id):
    # Extract session
    session = ICMYCSession()

    # Extract all users
    icmyc_users = session.query(IcmycUser).\
    filter(or_(IcmycUser.swachh_manch_user_id == None, IcmycUser.swachh_manch_user_id == 0)).\
    filter(IcmycUser.id >= from_id).\
    filter(IcmycUser.id <= to_id). \
    all()

    return icmyc_users


def find_or_create_sm_user(icmyc_user):
    try:
        # Extract session
        session = SwachhataSession()

        # Get users
        user = session.query(User).filter(User.mobile_number == icmyc_user.mobile_number).\
                filter(User.deleted == False).\
                first()
        
        if not user:
            user = User()
            user.mobile_number = icmyc_user.mobile_number
            user.mobile_number_verified = icmyc_user.otp_verified
            user.mobile_number_verified_at = icmyc_user.otp_verified_at
            user.mac_address = icmyc_user.mac_address
            user.last_login_at = icmyc_user.last_login_at
            user.last_login_ip = icmyc_user.sign_in_ip
            user.last_login_user_agent = icmyc_user.sign_in_user_agent
            user.last_login_channel = icmyc_user.sign_in_channel_id
            user.created_at = icmyc_user.created_at
            user.updated_at = icmyc_user.updated_at
            user.migrated_at = now()
            user.icmyc_user_id = icmyc_user.id
            
            # Persist data
            session.add(user)

            # Commit data
            session.commit()

            profile = store_user_in_mongo(user, icmyc_user)
            if not profile:
                print("Error in saving Mongo DB", user.id)
    finally:
        session.close()

    return user

# Store profile in Mongo
def store_user_in_mongo(user, icmyc_user):
    user_count = Profile.objects(user_id=user.id).count()
    channel = map_channel(icmyc_user.sign_up_channel_id)

    if user_count == 0:
        profile = Profile(
            user_id=user.id,
            full_name=icmyc_user.full_name,
            sign_up_with="mobile_number",
            sign_up_ip_address=icmyc_user.sign_up_ip,
            channels=[{"id": channel.id, "slug": channel.slug, 
                    "mac_address": icmyc_user.mac_address, "sign_up": True, "device_token": icmyc_user.device_token,
                    "last_login_at": icmyc_user.last_login_at,
                    "settings": {"email_notifications_preferred": True, 
                    "sms_notifications_preferred": True, 
                    "push_notifications_preferred": True}}],
            mobile_number=icmyc_user.mobile_number,
            mobile_number_verified=bool(int(icmyc_user.otp_verified)),
            mobile_number_verified_at=icmyc_user.otp_verified_at,
            mac_address=icmyc_user.mac_address,
            last_login_at=icmyc_user.last_login_at,
            last_login_ip=icmyc_user.sign_in_ip,
            last_login_user_agent=icmyc_user.sign_in_user_agent,
            last_login_channel=channel.slug,
            created_at=icmyc_user.created_at,
            updated_at=icmyc_user.updated_at,
            icmyc_user_id=icmyc_user.id,
            has_at_least_one_social_account=bool(int(icmyc_user.social_user))
            )
        profile.save()

        return True
    return False


def map_channel(channel_id):
    if channel_id == 1:
        slug = 'icmyc-portal'
    elif channel_id == 2:
        slug = 'icmyc-citizen-android'
    elif channel_id == 3:
        slug = 'icmyc-citizen-ios'
    else:
        slug = 'icmyc-portal'
    
    channel = Channel.objects(slug=slug).first()
    return channel

# Entry point
if __name__ == "__main__":
    from_id = input("From user ID:")
    to_id = input("To user ID:")
    try:
        from_id = int(from_id)
        to_id = int(to_id)
        if from_id > 0 and to_id > 0:
            icmyc_users = fetch_icmyc_users(from_id, to_id)
            print("***************************")
            for icmyc_user in icmyc_users:
                user = find_or_create_sm_user(icmyc_user)
                print(f'Swachhata user Id: {user.id}')
            print("***************************")
        else:
            print("Input should be positive integer")
    except ValueError:
        print("Input should be an integer")

