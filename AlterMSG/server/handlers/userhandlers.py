from handlers.json_util import JsonHandler
from database_tools.alchemy import CUsers, CContacts
from sqlalchemy import update
import secrets
from datetime import datetime, timedelta


class UserHandlers(JsonHandler):
    pass