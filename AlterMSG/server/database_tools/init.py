from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, DateTime, Boolean
from sqlalchemy import create_engine
from db_config import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE


engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))
meta = MetaData(bind=engine)

users = Table('users', meta,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('password', String),
              Column('email', String),
              Column('token', String),
              Column('creation_data', DateTime),
              Column('last_online', DateTime),
              Column('status', String),    # , ForeignKey('status_of_user.id')
              Column('role', String)   # , ForeignKey('user_roles.id')
              )

messages = Table('messages', meta,
                 Column('id', Integer, primary_key=True),
                 Column('group_to_user', Boolean, default=False),
                 Column('user_to_group', Boolean, default=False),
                 Column('send', String),
                 Column('recv', String),
                 Column('message', String),
                 Column('dtime', DateTime),
                 Column('delivered', Boolean, default=False)
                 )

contacts = Table('contacts', meta,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey('users.id')),
                 Column('contact', Integer, ForeignKey('users.id'))
                 )

groups = Table('groups', meta,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('creation_date', DateTime),
               Column('creater_user_id', ForeignKey('users.id')),
               Column('category_group', Integer, ForeignKey('category_group.id'))
               )

user_groups = Table('user_groups', meta,
                    Column('id', Integer, primary_key=True),
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('group_id', Integer, ForeignKey('groups.id')),
                    Column('status_user', String)
                    )

# user_roles = Table('user_roles', meta,
#                    Column('id', Integer, primary_key=True),
#                    Column('role_name', String)
#                    )

# status_of_user = Table('status_of_user', meta,
#                        Column('id', Integer, primary_key=True),
#                        Column('status_name', String)
#                        )

coll_group = Table('coll_group', meta,
                   Column('id', Integer, primary_key=True),
                   Column('collgroup_id', Integer, ForeignKey('groups.id')),
                   Column('group_id', Integer, ForeignKey('groups.id'))
                   )

category_group = Table('category_group', meta,
                       Column('id', Integer, primary_key=True),
                       Column('name', String)
                       )

meta.create_all(engine)
