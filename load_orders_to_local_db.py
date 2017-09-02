from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import TimeoutError, DBAPIError, DisconnectionError
import time
import os
import re
import logging
import argparse


VERBOSITY_TO_LOGGING_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
}

DB_URL = os.environ["DATABASE_URL"]


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
        logging.debug(e)
        logging.info('Something goes wrong. Trying reconnect to db')
        db.session.rollback()
    except DBAPIError as e:
        logging.debug(e)
        logging.info('Something goes wrong. Trying reconnect to db')
        db.session.rollback()
    except DisconnectionError as e:
        logging.debug(e)
        logging.info('Something goes wrong. Trying reconnect to db')
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
        logging.info('Rows normalized: {}\n'.format(len(not_normalized_orders)))


def get_args_from_terminal():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count', default=0)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args_from_terminal()
    logging_level = VERBOSITY_TO_LOGGING_LEVELS[args.verbose]
    logging.basicConfig(level=logging_level)
    session, order_class = create_session_and_model(DB_URL)
    time_amount = 60*5
    while True:
        not_normalized_orders = get_not_normalized_orders_from_db(session, order_class)
        normalize_orders_in_db(session, order_class, not_normalized_orders)
        print_new_orders_amount(not_normalized_orders)
        time.sleep(time_amount)
