from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask
import phonenumbers
import os


local_engine = create_engine(os.environ["DATABASE_URL"])
Local_session = sessionmaker(bind=local_engine)
local_session = Local_session()

remote_engine = create_engine('postgres://score:Rysherat2@shopscore.devman.org:5432/shop')
Remote_session = sessionmaker(bind=remote_engine)
remote_session = Remote_session()

BaseLocal = declarative_base()
BaseLocal.metadata.reflect(BaseLocal)

class LocalOrderModel(BaseLocal):
    __table__ = Base_class.metadata.tables['orders']

BaseRemote = declarative_base()
BaseLocal.metadata.reflect(BaseRemote)

class RemoteOrderModel(BaseRemote):
    __table__ = Base_class.metadata.tables['orders']


while True:
    lastest_confirmed_order_date = local_session.query(LocalOrderModel).order_by(desc(LocalOrderModel.confirmed)).first().confirmed
    new_orders = []
    try:
        new_orders = remote_session.query(RemoteOrderModel).filter(RemoteOrderModel).filter(
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
    time.sleep(60)
