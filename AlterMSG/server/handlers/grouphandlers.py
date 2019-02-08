from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CGroups, CGroupsUsers, CCollGroup, CCategoryGroup
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class GroupHandlers(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.json_data['action'] == 'created_group':
            self.created_group()
        elif self.json_data['action'] == 'update_group':
            self.update_group()
        elif self.json_data['action'] == 'deleted_group':
            self.deleted_group()
        elif self.json_data['action'] == 'add_user_group':
            self.add_user_group()
        elif self.json_data['action'] == 'delete_user_group':
            self.del_user_group()
        else:
            self.send_error(409, message='bad')

    # def created_group(self):
    #     if self.check_result:
    #         user = self.json_data['account_name']
    #         group_name = self.json_data['group_name']
    #         category = self.json_data['category_group']
    #         creater_user = self.db.query(CUsers).filter_by(name=user).first()
    #         result_group = self.db.query(CGroups).filter(CGroups.name == group_name).all()
    #         if len(result_group) == 0:
    #             if creater_user:
    #                 category_group = self.db.query(CCategoryGroup).filter(CCategoryGroup.name == category).first()
    #                 new_group = CGroups(name=group_name,
    #                                     category_group=category_group.id,
    #                                     creater_user_id=creater_user.id)
    #                 self.db.add(new_group)
    #                 self.db.commit()
    #                 group = self.db.query(CGroups).filter(CGroups.name == group_name).first()
    #                 new_user = CGroupsUsers(user_id=creater_user.id,
    #                                         group_id=group.id)
    #                 self.db.add(new_user)
    #                 self.db.commit()
    #                 self.set_status(201, reason='Created')
    #                 self.response['group_name'] = group.name
    #                 self.response['creation_date'] = str(group.creation_date)
    #                 self.write_json()
    #             else:
    #                 self.set_status(403, reason='User does not exist')
    #         else:
    #             self.send_error(400, message='Bad JSON, need group name')
    #     else:
    #         self.set_status(403, reason='User not registation')

    def created_group(self):
        if self.check_result:
            group_name = None
            category = None
            creater_user = None
            result_group = None
            try:
                user = self.check_result.name   # json_data['account_name']
                group_name = self.json_data['group_name']
                category = self.json_data['category_group']
                creater_user = self.db.query(CUsers).filter_by(name=user).first()
                result_group = self.db.query(CGroups).filter(CGroups.name == group_name).all()
            except Exception as e:
                self.send_error(400, message='Bad JSON')
            if result_group:
                self.send_error(400, message='A group with the same name already exists')
            else:
                if creater_user:
                    category_group = self.db.query(CCategoryGroup).filter(CCategoryGroup.name == category).first()
                    new_group = CGroups(name=group_name,
                                        category_group=category_group.id,
                                        creater_user_id=creater_user.id)
                    self.db.add(new_group)
                    self.db.commit()
                    group = self.db.query(CGroups).filter(CGroups.name == group_name).first()
                    new_user = CGroupsUsers(user_id=creater_user.id,
                                            group_id=group.id)
                    self.db.add(new_user)
                    self.db.commit()
                    self.set_status(201, reason='Created')
                    self.response['group_name'] = group.name
                    self.response['creation_date'] = str(group.creation_date)
                    self.write_json()
                else:
                    self.set_status(403, reason='User does not exist')
        else:
            self.set_status(403, reason='User not registation')

    def update_group(self):
        """ НЕПРОВЕРЕННО """
        pass

    def deleted_group(self):
        if self.check_result:

            user = self.check_result.name
            group_name = self.json_data['group_name']
            creater_user = self.db.query(CUsers).filter_by(name=user).first()
            result_group = self.db.query(CGroups).filter(CGroups.name == group_name).first()

            if (creater_user is None) or (result_group is None) or (group_name is None):
                self.send_error(400, message='Bad JSON')

            elif not creater_user:
                self.send_error(404, message='User not found')
            elif not result_group:
                self.send_error(404, message='Group not found')
            else:
                if result_group.creater_user_id == creater_user.id:

                    group = self.db.query(CGroups).filter(CGroups.name == group_name).one_or_none()
                    result_user = self.db.query(CGroupsUsers).filter(CGroupsUsers.group_id == group.id).delete()
                    result = self.db.query(CGroups).filter(CGroups.id == group.id).delete()
                    if not result:
                        self.set_status(404, 'Group does not exists')
                    else:
                        self.db.commit()
                        self.set_status(201, reason='Deleted')
                        self.response['group_delete'] = group.name
                        self.write_json()
                else:
                    self.set_status(403, reason='User does not exist')
        else:
            self.set_status(403, reason='User not registation')

    def add_user_group(self):
        if self.check_result:
            user = self.check_result
            result_group = None
            user_gr = None
            try:
                add_user = self.json_data['add_user']
                group_name = self.json_data['group_name']
                result_group = self.db.query(CGroups).filter(CGroups.name == group_name).first()
                user_gr = self.db.query(CUsers).filter(CUsers.email == add_user).first()
            except Exception as e:
                self.send_error(400, message='Bad JSON')

            if result_group.creater_user_id == user.id:
                user_group = CGroupsUsers(user_id=user_gr.id,
                                          group_id=result_group.id)
                self.db.add(user_group)
                self.db.commit()
                self.set_status(201, reason='OK')
                self.response['user'] = user_gr.email
                self.response['group'] = result_group.name
                self.write_json()
            else:
                self.send_error(403, message='No rights')
        else:
            self.set_status(403, message='User not registation')

    def del_user_group(self):
        if self.check_result:
            user = self.check_result
            result_group = None
            user_gr = None
            try:
                del_user = self.json_data['delete_user']
                group_name = self.json_data['group_name']
                result_group = self.db.query(CGroups).filter(CGroups.name == group_name).first()
                user_gr = self.db.query(CUsers).filter(CUsers.email == del_user).first()
            except Exception as e:
                self.send_error(400, message='Bad JSON')

            if result_group.creater_user_id == user.id:
                if not user_gr:
                    self.send_error(404, message='User in group not found')
                else:
                    delete_user = self.db.query(CGroupsUsers).filter(CGroupsUsers.user_id == user_gr.id).delete()
                    self.db.commit()
                    self.set_status(201, reason='OK')
                    self.response['group'] = result_group.name
                    self.response['delete_user'] = user_gr.email
                    self.write_json()
            else:
                self.send_error(403, message='No rights')
        else:
            self.set_status(403, message='User not registation')
