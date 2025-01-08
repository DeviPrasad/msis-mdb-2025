#
# create a venv, install mysql-connector, and test the program.
### python3 -m venv ~/teaching/mysql
### source ~/teaching/mysql/bin/activate
### pip3 install mysql-connector-python
#
# activate venv and run the program
## source ~/teaching/mysql/bin/activate
## python3 intro.py
#

import logging
import mysql.connector as msc


def init():
    logging.basicConfig(
        format="%(asctime)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S %p"
    )


def mysql8_perpared_stmt_create_neft_acc(conn, **cust):
    try:
        assert conn.is_connected()
        conn.start_transaction()
        cursor = conn.cursor(prepared=True)
        sql = "insert into cust_neft_acc values(%s,%s,%s,%s,%s,%s,default,%s)"
        cursor.execute(
            sql,
            (
                cust["cust_code"],
                cust["neft_acc"],
                cust["ifsc"],
                cust["status"],
                cust["acc_holder_name"],
                cust["msg"],
                cust["cuid"],
            ),
        )
        conn.commit()
    except Exception as ex:
        logging.error("mysql8_perpared_stmt_create_neft_acc - %s", ex)
        conn.rollback()


def mysql8_create_neft_acc(conn, **cust):
    try:
        assert conn.is_connected()
        conn.start_transaction()
        cursor = conn.cursor()
        cursor.execute(
            "insert into cust_neft_acc values('%s','%s','%s','%s','%s','%s',default,'%s')"
            % (
                cust["cust_code"],
                cust["neft_acc"],
                cust["ifsc"],
                cust["status"],
                cust["acc_holder_name"],
                cust["msg"],
                cust["cuid"],
            ),
        )
        conn.commit()
    except Exception as ex:
        logging.error("mysql8_create_neft_acc - %s", ex)
        conn.rollback()


def mysql8_connect(db_host, db_port, db_name, db_user, secret):
    try:
        conn = msc.connect(
            port=db_port,
            host=db_host,
            database=db_name,
            user=db_user,
            password=secret,
        )
        assert conn.is_connected()
        return conn
    except msc.Error as err:
        logging.error("mysql8_connect - %s", err)


def mysql8_close(conn):
    try:
        assert conn.is_connected()
        conn.close()
        assert not conn.is_connected()
    except Exception as ex:
        logging.error("mysql8_close - %s", ex)


def test_mysql8_connection():
    try:
        conn = mysql8_connect(
            "multicore.in",
            41526,
            "mdb_intro",
            "mdb_py_script",
            "{MdbPyScript!!2025/01/*}",
        )
        if conn is not None:
            assert conn.is_connected()
            mysql8_close(conn)
    except Exception as ex:
        logging.error("test_mysql8_connection - %s", ex)


def test_mysql8_insert_neft_acc():
    try:
        conn = mysql8_connect(
            "multicore.in",
            41526,
            "mdb_intro",
            "mdb_py_script",
            "{MdbPyScript!!2025/01/*}",
        )
        if conn is not None:
            mysql8_create_neft_acc(
                conn,
                cust_code="0914725006808325",
                neft_acc="99305528041362",
                ifsc="RXTC1740301",
                status="ok",
                acc_holder_name="Moxie Morlinspike",
                msg="account is verified and is active",
                cuid="MDB0025001234",
            )
            mysql8_perpared_stmt_create_neft_acc(
                conn,
                cust_code="0939825006808325",
                neft_acc="14305523040802",
                ifsc="SBI01740301",
                status="ok",
                acc_holder_name="Ravishankar S",
                msg="verified and active",
                cuid="MDB0025005678",
            )
            mysql8_close(conn)
    except Exception as ex:
        logging.error("test_mysql8_insert_neft_acc - %s", ex)


init()
test_mysql8_connection()
test_mysql8_insert_neft_acc()
