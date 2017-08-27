from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
import phonenumbers
import datetime
import os
import sqlalchemy
import time

local_engine = create_engine(os.environ["DATABASE_URL"])
Local_session = sessionmaker(bind=local_engine)
local_session = Local_session()

BaseLocal = declarative_base()
BaseLocal.metadata.reflect(local_engine)

class LocalOrderModel(BaseLocal):
    __table__ = BaseLocal.metadata.tables['orders']


remote_engine = create_engine('postgres://score:Rysherat2@shopscore.devman.org:5432/shop')
Remote_session = sessionmaker(bind=remote_engine)
remote_session = Remote_session()

BaseRemote = declarative_base()
BaseRemote.metadata.reflect(remote_engine)

class RemoteOrderModel(BaseRemote):
    __table__ = BaseRemote.metadata.tables['orders']

lastest_confirmed_order_date = datetime.datetime.now() - datetime.timedelta(hours=4)
