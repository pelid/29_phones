from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import TimeoutError
import time
import os
import re


def create_session_and_model(db_url_path):
    engine = create_engine(db_url_path)
    session = sessionmaker(bind=engine)()
    base_class = declarative_base()
    base_class.metadata.reflect(engine)

    class order_class(base_class):
        __table__ = base_class.metadata.tables['orders']

    return session, order_class


def get_not_normalized_orders_from_db(session, order_class):
    not_normalized_orders = []
    try:
        not_normalized_orders = session.query(order_class).filter(
                                    order_class.normalized_phone_number == None).all()
    except TimeoutError as e:
        print(e, '\nTrying reconnect to db')
        db.session.rollback()
    return not_normalized_orders


def normalize_orders_in_db(session, order_class, not_normalized_orders):
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
    session, order_class = create_session_and_model(db_url)
    time_amount = 60*5
    while True:
        not_normalized_orders = get_not_normalized_orders_from_db(session, order_class)
        normalize_orders_in_db(session, order_class, not_normalized_orders)
        print_new_orders_amount(not_normalized_orders)
        time.sleep(time_amount)
