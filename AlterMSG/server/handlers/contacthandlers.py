from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class ContactHandlers(JsonHandler):
    def prepare(self):
        super().prepare()
        self.check_result = self._token_check()

    def post(self):
        if self.json_data['action'] == 'add_contact':
            self.add_contact()
        elif self.json_data['action'] == 'deleted_contact':
            self.deleted_contact()
        elif self.json_data['action'] == 'contact_list':
            self.contact_list()
        else:
            self.send_error(409, message='bad')

    def add_contact(self):
        if self.check_result:
            exists_contact = None
            try:
                contact = self.json_data['contact_email']
                exists_contact = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
            except:
                self.send_error(400, reason='No or bad request body')
            if exists_contact is None:
                self.set_status(404, 'User does not exists')
            else:
                result = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.id,
                                                         CContacts.contact == exists_contact.id).first()
                if result is None:
                    new_contact = CContacts(user_id=self.check_result.id, contact=exists_contact.id)
                    self.db.add(new_contact)
                    self.db.commit()

                    self.set_response(exists_contact)
                    self.write_json()
                    self.set_status(201, 'Added')
                else:
                    self.set_status(409, 'Contact already in list')

    def deleted_contact(self):
        if self.check_result:
            result = None
            result_db = None
            try:
                contact = self.json_data['contact_email']
                result = self.db.query(CUsers).filter(CUsers.email == contact).one_or_none()
                result_db = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.id,
                                                            CContacts.contact == result.id).delete()
            except:
                self.send_error(400, reason='No or bad request body')
            if result_db is None or result is None:
                self.set_status(404, 'Not in your contact list')
            else:
                self.db.commit()
                self.set_status(200)
                self.response['deleted_contact_id'] = result.id
                self.response['deleted_contact_name'] = result.name
                self.write_json()
        else:
            self.send_error(400, reason='No or bad request body')

    def contact_list(self):
        if self.check_result:
            contact_l = []
            result_db = None
            try:
                result_db = self.db.query(CContacts).filter(CContacts.user_id == self.check_result.id).all()
            except:
                self.send_error(400, reason='No or bad request body')
            for c in result_db:
                contact = self.db.query(CUsers).filter(CUsers.id == c.contact).first()
                contact_l.append(contact.email)
            if not result_db:
                self.send_error(404, reason='Not in your contact list')
            else:
                self.set_status(200)
                self.response['contact_list'] = contact_l
                self.response['check_list'] = len(contact_l)
                self.write_json()
        else:
            self.send_error(400, reason='No or bad request body')

    def update_contact(self):
        pass
