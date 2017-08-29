from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import TimeoutError
import phonenumbers
import time
import datetime
import os



def create_session_and_model(db_url_path):
    engine = create_engine(db_url_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    Base.metadata.reflect(engine)

    class Model(Base):
        __table__ = Base.metadata.tables['orders']

    return session, Model


def get_new_order_list_from_remote_db(remote_session, RemoteOrderModel):
    new_orders = []
    try:
        new_orders = remote_session.query(RemoteOrderModel).filter(
                                    RemoteOrderModel.status != "DRAFT").filter(
                                    RemoteOrderModel.confirmed > lastest_confirmed_order_date).all()
    except TimeoutError as e:
        print(e, '\nTrying reconnect to db')
        db.session.rollback()
    return new_orders


def insert_new_orders_to_db(local_session, LocalOrderModel, new_orders, table_names_list):
    for new_order in new_orders:
        order_dict = {x: y for x, y in new_order.__dict__.items() if x in table_names_list }
        normalized_phone_number = phonenumbers.parse(new_order.contact_phone, 'RU').national_number
        order_dict.update({'normalized_phone_number': str(normalized_phone_number)})
        local_session.add(LocalOrderModel(**order_dict))
    local_session.commit()


if __name__ == "__main__":
    local_db_url = os.environ["DATABASE_URL"]
    remote_db_url = 'postgres://score:Rysherat2@shopscore.devman.org:5432/shop'
    lastest_confirmed_order_date = datetime.datetime.now() - datetime.timedelta(hours=4)
    local_session, LocalOrderModel = create_session_and_model(local_db_url)
    remote_session, RemoteOrderModel = create_session_and_model(remote_db_url)
    table_names_list = LocalOrderModel.__table__.__dict__['columns'].keys()
    while True:
        if len(local_session.query(LocalOrderModel).all()) != 0:
            lastest_confirmed_order_date = local_session.query(LocalOrderModel).order_by(
                                                                    LocalOrderModel.confirmed.desc()).first().confirmed
        new_orders = get_new_order_list_from_remote_db(remote_session, RemoteOrderModel)
        insert_new_orders_to_db(local_session, LocalOrderModel, new_orders, table_names_list)
        if new_orders:
            print('записей вставлено: {}'.format(len(new_orders)))
        time.sleep(10)
