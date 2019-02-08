from database_tools.alchemy import CUsers, CUserStatus, CUserRoles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE
from datetime import datetime, timedelta

import hashlib
from salt import salt
import secrets


def token_expiration():
    today = datetime.now()
    days = timedelta(days=5)
    token_expire = (today + days)
    return token_expire


db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)

engine = create_engine(db_address)
Session = sessionmaker(bind=engine)
session = Session()

name = 'tester'
password = hashlib.sha256('qwerty'.encode() + salt.encode()).hexdigest()
email = 'mte@gmail.com'
token = secrets.token_hex(8)
today = datetime.now()
# status = session.query(CUserStatus).filter(CUserStatus.status_name == 'online').first()
# role = session.query(CUserRoles).filter(CUserRoles.role_name == 'admin').first()
time = token_expiration()

add_user = CUsers(name='Chief',
                  password=password,
                  email=email,
                  token=token,
                  creation_data=today,
                  last_online=today,
                  # tokenexp=time,
                  status='not confirm',
                  role='admin')

session.add(add_user)
session.commit()

add_user = CUsers(name='tester',
                  password=password,
                  email=email,
                  token=token,
                  creation_data=today,
                  last_online=today,
                  # tokenexp=time,
                  status='not confirm',
                  role='user')

session.add(add_user)
session.commit()
