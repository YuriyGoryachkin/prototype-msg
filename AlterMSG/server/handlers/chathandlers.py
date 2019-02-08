from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts, CMessages, CGroups, CGroupsUsers
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class ChatHandlers(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.json_data['action'] == 'user':
            self.user_to_user()
        elif self.json_data['action'] == 'group':
            self.user_to_group()
        elif self.json_data['action'] == 'check_message':
            self.check_message()
        else:
            self.send_error(409, message='bad')

    def user_to_user(self):
        if self.check_result:
            try:
                send = self.check_result
                recv = self.db.query(CUsers).filter(CUsers.email == self.json_data['recv']).first()
                message = self.json_data['message']
                dtime = datetime.now()
                if recv:
                    chat = CMessages(message=message,
                                     send=send.email,
                                     recv=recv.email,
                                     dtime=dtime,
                                     delivered=False)
                    self.db.add(chat)
                    self.db.commit()
                    self.set_status(200, reason='message OK')
                    self.response['deliv_to_DB'] = 'OK'
                    self.write_json()
                else:
                    self.send_error(404, message='Recipient not found')

            except Exception:
                self.send_error(400, message='Bad JSON')

    def user_to_group(self):
        if self.check_result:
            try:
                send = self.check_result
                recv = self.db.query(CGroups).filter(CGroups.name == self.json_data['recv']).first()
                message = self.json_data['message']
                dtime = datetime.now()
                if recv:
                    chat = CMessages(message=message,
                                     user_to_group=True,
                                     send=send.email,
                                     recv=recv.name,
                                     dtime=dtime,
                                     delivered=True)
                    self.db.add(chat)
                    self.db.commit()
                    self._grouptouser(send, recv, message)
                    self.set_status(200, reason='OK')
                    self.response['deliv_to_DB'] = 'OK'
                    self.write_json()
                else:
                    self.send_error(404, message='Recipient not found')
            except Exception:
                self.send_error(400, message='Bad JSON')

    def check_message(self):
        if self.check_result:
            result = {}
            dict_mes = []
            deliv = False
            result_db = self.db.query(CMessages).filter(CMessages.recv == self.check_result.email,
                                                        CMessages.delivered == deliv)
            if result_db is None:
                self.send_error(403, reason='No undelivered messages in DB')
            else:
                for r in result_db.all():
                    if r.group_to_user:
                        result['group'] = True
                    result['send'] = r.send
                    result['message'] = r.message
                    result['dtime'] = str(r.dtime)
                    dict_mes.append(result)
                if len(dict_mes) == 0:
                    self.set_status(200, reason='No undelivered messages')
                    self.response['count_message'] = len(dict_mes)
                    self.write_json()
                else:
                    self._update_delivered(result_db)
                    self.set_status(200, reason='OK')
                    self.response['check_message'] = dict_mes
                    self.response['count_message'] = len(dict_mes)
                    self.write_json()

    def _update_delivered(self, up_mes_del):
        up_mes_del.update({'delivered': True}, synchronize_session='evaluate')
        self.db.commit()

    def _grouptouser(self, send, recvgroup, mes):
        send_group = recvgroup
        send_user = send
        message = mes
        result_db = self.db.query(CGroupsUsers).filter(CGroupsUsers.group_id == send_group.id).all()
        for user in result_db:
            user2 = self.db.query(CUsers).filter(CUsers.id == user.user_id).first()
            chat2 = CMessages(message=[send_user.email, message],
                              group_to_user=True,
                              send=str(send_group.name),
                              recv=user2.email,
                              dtime=datetime.now(),
                              delivered=False)
            self.db.add(chat2)
            self.db.commit()



