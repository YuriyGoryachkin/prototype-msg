from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class MainHandlers(JsonHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        if self.json_data['action'] == 'registration':
            self.registration()
        elif self.json_data['action'] == 'authorization':
            self.authorization()
        else:
            self.send_error(409, message='bad')

    def put(self):
        check_result = self._token_check()

    def registration(self):
        try:
            result_email = self.db.query(CUsers.email).filter(CUsers.email == str(self.json_data['email'])).all()
            if len(result_email) > 0:
                message = 'Conflict, mail exist'
                self.send_error(409, message=message)
                print(message)
                return
        except KeyError:
            self.send_error(400, message='Bad JSON, email need')
        try:
            result = self.db.query(CUsers.name).filter(
                CUsers.name == self.json_data['account_name']).one_or_none()
            if result is None:
                user = self.json_data['account_name']
                password = self.json_data['password']
                password = self._create_sha(password)
                email = self.json_data['email']
                token = secrets.token_hex(8)
                creation_data = datetime.now()
                status = 'not confirm'
                user = CUsers(name=user, password=password,
                              email=email, token=token,
                              creation_data=creation_data, last_online=creation_data,
                              status=status, role='user')
                self.db.add(user)
                self.db.commit()
                self.set_status(201, reason='Created')
                self.response['token'] = token
                self.write_json()
            else:
                message = 'Conflict, user exists'
                self.send_error(409, message=message)
                print(message)

        except Exception as e:
            self.send_error(400, message='Bad JSON, need account_name')

    def authorization(self):
        check_result = self._token_check()  # ПЕРЕДЕЛАТЬ ПРОВЕРКУ ТОКЕНА
        if check_result:
            login = self.json_data['account_name']
            password = self.json_data['password']
            password = self._create_sha(password)
            exists = self.db.query(CUsers).filter_by(name=login).all()
            if exists:
                result_db = self.db.query(CUsers.password).filter_by(name=login).first()[0]
                if password == result_db:
                    token = secrets.token_hex(8)
                    last_online = datetime.now()
                    status = 'confirm'
                    query = update(CUsers).where(CUsers.name == login).values(token=token,
                                                                              last_online=last_online,
                                                                              status=status)
                    self.db.execute(query)
                    self.db.commit()
                    self.set_status(200)
                    self.response['token'] = token
                    self.write_json()
                else:
                    self.set_status(403, 'Incorrect password')

            else:
                self.set_status(403, reason='Login or password incorrect')
        else:
            self.set_status(403, reason='User not registation')
