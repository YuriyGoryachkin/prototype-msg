from sqlalchemy import Column, Integer, Unicode, UniqueConstraint, ForeignKey, MetaData, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

CBase = declarative_base()


class CUsers(CBase):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(Unicode())
    password = Column(Unicode())
    email = Column(Unicode())
    token = Column(Unicode())
    creation_data = Column(DateTime())
    last_online = Column(DateTime())
    check_1 = UniqueConstraint('name')
    check_2 = UniqueConstraint('email')
    status = Column(Unicode())  # , ForeignKey('status_of_user.id')
    role = Column(Unicode())  # , ForeignKey('user_roles._id')

    def __repr__(self):
        return 'CUsers: id = %d, account_name = %s, email = %s' % (self.id, self.name, self.email)


# class CUserStatus(CBase):
#     __tablename__ = 'status_of_user'
#
#     id = Column(Integer(), primary_key=True)
#     name = Column(Unicode())
#
#     def __repr__(self):
#         return 'CUserStatus: id = %d, status = %s' % (self.id, self.name)


# class CUserRoles(CBase):
#     __tablename__ = 'user_roles'
#
#     id = Column(Integer(), primary_key=True)
#     name = Column(Unicode())
#
#     # p_role_id = relationship('CUsers', foreign_keys=[role_id])
#
#     def __repr__(self):
#         return 'CUserStatus: role_id = %d, role_name = %s' % (self.role_id, self.role_name)


class CMessages(CBase):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    message = Column(Unicode())
    group_to_user = Column(Boolean(), default=False)
    user_to_group = Column(Boolean(), default=False)
    send = Column(Unicode())
    recv = Column(Unicode())
    dtime = Column(DateTime(), default=datetime.datetime.utcnow())
    delivered = Column(Boolean(), default=False)

    def __repr__(self):
        return 'CMessages: id = {}, send = {}, recv = {}, message = {}'.format(
            self.id, self.send, self.recv, self.message)


class CContacts(CBase):
    __tablename__ = 'contacts'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    contact = Column(Integer(), ForeignKey('users.id'))

    p_user_id = relationship('CUsers', foreign_keys=[user_id])
    p_contact = relationship('CUsers', foreign_keys=[contact])

    def __repr__(self):
        return 'CContacts: id = %d, user_id = %d, contact = %d' % (self.id, self.user_id, self.contact)


class CGroups(CBase):
    __tablename__ = 'groups'
    id = Column(Integer(), primary_key=True)
    creation_date = Column(DateTime(), default=datetime.datetime.utcnow())
    name = Column(Unicode())
    creater_user_id = Column(Integer(), ForeignKey('users.id'))
    category_group = Column(Integer(), ForeignKey('category_group.id'))
    check_1 = UniqueConstraint('name')

    p_creater_user_id = relationship('CUsers', foreign_keys=[creater_user_id])
    p_category_group = relationship('CCategoryGroup', foreign_keys=[category_group])

    def __repr__(self):
        return 'CGroups: id = {},  name = {}, creation_date = {}'.format(self.id, self.name, self.creation_date)


class CCollGroup(CBase):
    """ Коллекция групп ("группы в группе")"""
    __tablename__ = 'coll_group'
    id = Column(Integer(), primary_key=True)
    collgroup_id = Column(Integer(), ForeignKey('groups.id'))
    group_id = Column(Integer(), ForeignKey('groups.id'))

    p_collgroup_id = relationship('CGroups', foreign_keys=[collgroup_id])
    p_group_id = relationship('CGroups', foreign_keys=[group_id])

    def __repr__(self):
        return 'CCollGroup: collgroup_id = {}, group_id = {}'.format(self.collgroup_id, self.group_id)


class CCategoryGroup(CBase):
    """ Категории групп(обычная или мультигруппа """
    __tablename__ = 'category_group'
    id = Column(Integer(), primary_key=True)
    name = Column(Unicode())

    # p_category_id = relationship('CGroups', foreign_keys=[category_id])

    def __repr__(self):
        return 'CCategoryGroup: category_id = {}, category_name = {}'.format(self.id, self.name)


class CGroupsUsers(CBase):
    __tablename__ = 'user_groups'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    group_id = Column(Integer(), ForeignKey('groups.id'))

    p_user_id = relationship('CUsers', foreign_keys=[user_id])
    p_group_id = relationship('CGroups', foreign_keys=[group_id])

    def __repr__(self):
        return 'CGroupUsers: user_id = {}, group_id = {}'.format(self.user_id, self.group_id)
