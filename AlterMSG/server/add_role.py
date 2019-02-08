from database_tools.alchemy import CUserRoles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_tools.db_config import POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_BASE

db_address = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                                POSTGRES_PORT,
                                                                POSTGRES_BASE)

engine = create_engine(db_address)
Session = sessionmaker(bind=engine)
session = Session()

# add_role = CUserRoles(role_name='admin')
# session.add(add_role)
# session.commit()
#
# add_role = CUserRoles(role_name='teacher')
# session.add(add_role)
# session.commit()
#
# add_role = CUserRoles(role_name='student')
# session.add(add_role)
# session.commit()
#
# add_role = CUserRoles(role_name='admin_group')
# session.add(add_role)
# session.commit()
#
# add_role = CUserRoles(role_name='user')
# session.add(add_role)
# session.commit()

session.add_all([CUserRoles(role_name='admin'),
                 CUserRoles(role_name='teacher'),
                 CUserRoles(role_name='student'),
                 CUserRoles(role_name='admin_group'),
                 CUserRoles(role_name='user')])
session.commit()
