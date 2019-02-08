from database_tools.alchemy import CUserStatus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)

engine = create_engine(db_address)
Session = sessionmaker(bind=engine)
session = Session()

# add_status = CUserStatus(status_name='online')
# session.add(add_status)
# session.commit()
#
# add_status = CUserStatus(status_name='offline')
# session.add(add_status)
# session.commit()
#
# add_status = CUserStatus(status_name='banned')
# session.add(add_status)
# session.commit()
#
# add_status = CUserStatus(status_name='not confirmed')
# session.add(add_status)
# session.commit()

session.add_all([CUserStatus(status_name='online'),
                 CUserStatus(status_name='offline'),
                 CUserStatus(status_name='banned'),
                 CUserStatus(status_name='not confirmed'),
                 ])
session.commit()