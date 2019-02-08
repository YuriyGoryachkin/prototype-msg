from database_tools.alchemy import CGroups, CCollGroup, CCategoryGroup, CUsers, CContacts, CGroupsUsers, CMessages, CBase
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from database_tools.db_connect import POSTGRES_SERVER, POSTGRES_PORT, POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_BASE
from datetime import datetime

engine = create_engine(
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(POSTGRES_LOGIN, POSTGRES_PASS, POSTGRES_SERVER,
                                                       POSTGRES_PORT,
                                                       POSTGRES_BASE))


Session = sessionmaker(bind=engine)
session = Session()

# out = session.query(CUsers).filter(CUsers.username == 'tester3').one()
#
#
#
# print('out - {}'.format(out))
#
# print('uid - {}'.format(out.uid))
#
# print('email - {}'.format(out.email))
# print('date - {}'.format(datetime.utcnow()))
# #
# category_multi = session.query(CCategoryGroup).filter(CCategoryGroup.category_name == 'Multi').first()
# category_single = session.query(CCategoryGroup).filter(CCategoryGroup.category_name == 'Single').first()
# print('category - {}'.format(category_multi))
# #
# # supergroup = CGroups(creation_date=datetime.utcnow(),
# #                      group_name='test_group3',
# #                      creater_user_id=out.uid,
# #                      category_group=category.category_id)
# #
# # session.add(supergroup)
# # session.commit()
# out_group = session.query(CGroups).filter(CGroups.creater_user_id == out.uid).all()
# print('out_group - {}'.format(out_group))
#
# grand_group = session.query(CGroups).filter(CGroups.category_group == category_multi.category_id).first()
# add_group = session.query(CGroups).filter(CGroups.category_group == category_single.category_id).first()
# coll_gr = CCollGroup(collgroup_id=grand_group.gid,
#                      group_id=add_group.gid)
# session.add(coll_gr)
# session.commit()

# ''' Удаление таблиц '''
# CBase.metadata.drop_all(engine)

# group = session.query(CGroups).filter(CGroups.name == 'group5').one()
# print(group.id, group.name, group.creation_date)
#
# query = update(CUsers).where(CUsers.username == login).values(token=token,
#                                                               tokenexp=token_exp,
#                                                               status_id=status.usid)
# self.db.execute(query)

# dictmes = {}
# listmes = []
# result =session.query(CMessages).filter(CMessages.recv == 'mong2@gmail.com').all()
# print(result)
# for m in result:
#     dictmes['recv'] = m.recv
#     dictmes['message'] = m.message
#     dictmes['dtime'] =str(m.dtime)
#     timestr = str(m.dtime)
#     listmes.append(dictmes)
#
# print(listmes)
#
# print(datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S'))

user = session.query(CUsers).filter(CUsers.id == 3).first()
print(user.email)
message = 'sdfghjklkjhg'
chat = CMessages(message=[user.email, message],
                 group_to_user=True,
                 send='group4',
                 recv=user.email,
                 dtime=datetime.now(),
                 delivered=False)
print(chat)
session.add(chat)
print(chat)
session.commit()
print(chat)
print('1')