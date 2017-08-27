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

while True:
    if len(local_session.query(LocalOrderModel).all()) != 0:
        lastest_confirmed_order_date = local_session.query(LocalOrderModel).order_by(LocalOrderModel.confirmed.desc()).first().confirmed

    new_orders = []
    try:
        new_orders = remote_session.query(RemoteOrderModel).filter(RemoteOrderModel.status != "DRAFT").filter(
                                RemoteOrderModel.confirmed > lastest_confirmed_order_date).all()
    except sqlalchemy.exc.TimeoutError as e:
        print(e)
        print('Trying reconnect to db')
        db.session.rollback()
    for new_order in new_orders:
        order_dict = new_order.__dict__
        normalized_phone_number = phonenumbers.parse(new_order.contact_phone, 'RU').national_number
        order_dict.update({'normalized_phone_number': normalized_phone_number})
        local_session.add(LocalOrderModel(**order_dict))
    local_session.commit()
    print('orders are written:\n{}'.format([x.id for x in new_orders]))
    time.sleep(10)
