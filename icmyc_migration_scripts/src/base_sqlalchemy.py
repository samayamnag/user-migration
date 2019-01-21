from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import getenv


swachhata_engine = create_engine(
    f'mysql+pymysql://'
    f'{getenv("SWACHHATA_MYSQL_DB_USERNAME")}:{getenv("SWACHHATA_MYSQL_DB_PASSWORD")}'
    f'@{getenv("SWACHHATA_MYSQL_DB_HOST")}/{getenv("SWACHHATA_MYSQL_DB_NAME")}'
    )
icmyc_engine = create_engine(
    f'mysql+pymysql://'
    f'{getenv("ICMYC_MYSQL_DB_USERNAME")}:{getenv("ICMYC_MYSQL_DB_PASSWORD")}'
    f'@{getenv("ICMYC_MYSQL_DB_HOST")}/{getenv("ICMYC_MYSQL_DB_NAME")}'
    )
SwachhataSession = sessionmaker(bind=swachhata_engine)
ICMYCSession = sessionmaker(bind=icmyc_engine)
Base = declarative_base()