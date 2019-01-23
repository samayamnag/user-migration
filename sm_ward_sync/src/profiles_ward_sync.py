from mongoengine import connect
from dotenv import load_dotenv
from utils import getenv, now
from models import Ward, City
from base_sqlalchemy import Base, SmMetaDataSession
from profile import Profile

# Swachhata Mongo connection
connect(
    getenv('SM_MONGO_DB_NAME'),
    host=getenv("SM_MONGO_DB_HOST"),
    port=int(getenv("SM_MONGO_DB_PORT")),
    username=getenv('SM_MONGO_DB_USERNAME'),
    password=getenv("SM_MONGO_DB_PASSWORD")
    )

def fetchProfiles(fromUserId, toUserId):
    return Profile.objects(
        user_id__gte=fromUserId,
        user_id__lte=toUserId,
        ward_id__in=[],
        ward_id__ne=300,
        city_id__nin=[None, 4500],
    )

def updateProfile(profile):
    # Extract session
    session = SmMetaDataSession()

    # Get Ward - MySQL
    ward = session.query(Ward).filter(Ward.meta_data_ward_id == profile.ward_id).\
            first()

    if ward:
        if profile.channels:
            if type(profile.channels) is not list:
                profile.channels = [profile.channels]
                profile.save()
        # update profile model
        profile.mapped_ward_id = ward.id
        profile.mapped_ward_number = ward.ward_number
        profile.mapped_ward = ward.ward_translations[0].title
        profile.mapped_city_id = ward.city_id
        profile.mapped_city = ward.city.title
        profile.mapped_district_id = ward.city.district_id
        profile.mapped_district = ward.city.district_title
        profile.mapped_state_id = ward.city.state_id
        profile.mapped_state = ward.city.state_title
        profile.ward_not_in_sync = True
        profile.save()
    
    # Close session
    session.close()

    return profile

# Entry point
if __name__ == "__main__":
    from_id = input("From user ID:")
    to_id = input("To user ID:")
    try:
        from_id = int(from_id)
        to_id = int(to_id)
        if from_id > 0 and to_id > 0:
            profiles = fetchProfiles(from_id, to_id)
            print("***************************")
            for profile in profiles:
                profile = updateProfile(profile)
                print(f"Ward updated for profile: {profile.user_id}")            
            print("***************************")
        else:
            print("Input should be positive integer")
    except ValueError:
        print("Input should be an integer")

