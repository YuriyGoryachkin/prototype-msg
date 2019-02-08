from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CGroups, CGroupsUsers, CCollGroup, CCategoryGroup
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class TestHandlers(JsonHandler):
    def prepare(self):
        super().prepare()

    def post(self):
        check_result = self._token_check()
        if check_result:
            try:
                for key in self.json_data.keys():
                    self.response[key] = self.json_data[key]

                self.write_json()
            except Exception as e:
                message = 'Bad JSON:'
                self.send_error(400, message=message)
        else:
            self.set_status(403, reason='User not registation')
