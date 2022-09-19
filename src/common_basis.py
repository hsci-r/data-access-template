import keyring
import getpass
import sqlalchemy
import os
import yaml
from hereutil import here
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import Engine, Connection


def get_connection() -> (Engine, Connection):
    eng = None
    con = None
    while con is None:
        with here("db_params.yaml").open('r') as f:
            db_params = yaml.safe_load(f)
        password = os.environ.get("DB_PASS")
        if password is None:
            try:
                password = keyring.get_password(db_params['db_name'], "DB_PASS")
            except keyring.errors.NoKeyringError:
                pass
        try:
            eng = sqlalchemy.create_engine(
                "mariadb+pymysql://" + db_params['db_user'] + ":" + password + "@" + db_params['db_host'] + "/" +
                db_params['db_name'] + "?charset=utf8mb4&autocommit&local_infile",
                future=True
            )
            con = eng.connect()
        except SQLAlchemyError as err:
            eng = None
            con = None
            password = getpass.getpass(f"Database password (connection attempt failed with {err}): ")
            try:
                if keyring.get_password(db_params['db_name'], "DB_PASS") is not None:
                    keyring.delete_password(db_params['db_name'], "DB_PASS")
                keyring.set_password(db_params['db_name'], "DB_PASS", password)
            except keyring.errors.NoKeyringError:
                pass
    return eng, con


eng, con = get_connection()
del get_connection


def set_session_storage_engine(con: Connection, engine: str):
    con.execute(text("SET SESSION storage_engine="+engine))


__all__ = ["eng", "con", "set_session_storage_engine"]
