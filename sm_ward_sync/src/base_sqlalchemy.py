from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils import getenv

sm_meta_data_engine = create_engine(
    f'mysql+pymysql://'
    f'{getenv("SM_META_DATA_MYSQL_DB_USERNAME")}:{getenv("SM_META_DATA_MYSQL_DB_PASSWORD")}'
    f'@{getenv("SM_META_DATA_MYSQL_DB_HOST")}/{getenv("SM_META_DATA_MYSQL_DB_NAME")}'
    )
SmMetaDataSession = sessionmaker(bind=sm_meta_data_engine)
Base = declarative_base()