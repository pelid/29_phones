from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import TimeoutError
import time
import os
import re


def create_session_and_model(db_url_path):
    engine = create_engine(db_url_path)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()
    Base.metadata.reflect(engine)

    class Model(Base):
        __table__ = Base.metadata.tables['orders']

    return session, Model


def get_not_normalized_orders_list_from_db(session, Model):
    not_normalized_orders = []
    try:
        not_normalized_orders = session.query(Model).filter(
                                    Model.normalized_phone_number == None).all()
    except TimeoutError as e:
        print(e, '\nTrying reconnect to db')
        db.session.rollback()
    return not_normalized_orders


def normalize_orders_in_db(session, Model, not_normalized_orders):
    for order in not_normalized_orders:
        national_num_only_len = 10
        normalized_phone_number = ''.join(re.findall(r'\d+',
                                          order.contact_phone))[-national_num_only_len:]
        order.normalized_phone_number = str(normalized_phone_number)
    session.commit()


def print_new_orders_amount(not_normalized_orders):
    if not_normalized_orders:
        print('Rows inserted: {}\n'.format(len(not_normalized_orders)))


if __name__ == "__main__":
    db_url = os.environ["DATABASE_URL"]
    session, Model = create_session_and_model(db_url)
    time_amount = 60*5
    while True:
        not_normalized_orders = get_not_normalized_orders_list_from_db(session, Model)
        normalize_orders_in_db(session, Model, not_normalized_orders)
        print_new_orders_amount(not_normalized_orders)
        time.sleep(time_amount)
