##
## Title: python3 and mongodb
## Install Instructions:
## $ python3 -m venv ~/teaching/mongo
## $ source ~/teaching/mongo/bin/activate
## $ python3 -m pip install pymongo

import logging
from uuid import UUID
from decimal import *
from datetime import datetime
import bson
import pymongo

logger = None


def init_logger(name):
    global logger
    logging.basicConfig(
        format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p"
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)


class MongoDB:
    def __init__(self, url, port):
        self.mcl = None
        self.session = None
        try:
            self.mcl = pymongo.MongoClient(url + ":" + str(port))
            self.session = self.mcl.start_session(causal_consistency=True)
            logger.info("KoinDB connection opened")
        except Exception as ex:
            logger.error("MongoDB connection: %s" % str(ex))

    def haveConnection(self):
        return self.mcl != None

    def db_names(self):
        return self.mcl.list_database_names()

    def close(self):
        try:
            if self.mcl != None:
                self.mcl.close()
            logger.warning("KoinDB connection closed")
        except Exception as ex:
            logger.error(ex)


class KoinDB(MongoDB):
    def __init__(self, url, port):
        self.db = None
        try:
            MongoDB.__init__(self, url, port)
            self.db = self.getKoinDBInstance()
            print(self.db)
        except:
            logger.error("koinDB missing")

    def getKoinDBInstance(self):
        try:
            self.db_names().index("koinDB")
            return self.mcl["koinDB"]
        except:
            logger.error("koinDB not found")
        return None

    def haveKoinDB(self):
        return self.db != None

    def get_loan_agreements(self):
        return self.db.loan_agreements

    def get_loan_agreement(self, loan_id):
        return self.db.loan_agreements.find_one(
            {"_id": loan_id}, session=self.session, skip=0
        )

    def create_new_loan_agreement(self, agreement):
        try:
            logger.info("create_new_loan_agreement - 1 %s" % agreement.to_dict())
            self.db.loan_agreements.insert_one(
                bson.BSON.encode(agreement.to_dict()), session=self.session
            )
            # self.db.loan_agreements.insert_one((agreement.to_dict()))
            logger.info("create_new_loan_agreement - 2")
        except Exception as ex:
            logger.error("create_new_loan_agreement : {}" % ex)


class LoanLender:
    def __init__(self, bson_lender):
        self.id = UUID(bytes=bson_lender["id"])
        self.amount_contributed = bson_lender["amount_contributed"]
        self.disbursed = bson_lender["disbursed"]
        self.status = bson_lender["status"]
        self.amount_received = bson_lender["amount_received"]

    def add_amount_received(self, amt):
        amount = Decimal(amt)
        if amount < 0:
            raise Exception("Invalid amount")
        self.amount_received = self.amount_received.to_decimal() + Decimal(amt)

    def __str__(self):
        return "\t(id:{}, contribution: {}, , received: {}, disbursed: {}, active: {})".format(
            self.id,
            self.amount_contributed,
            self.amount_received,
            self.disbursed,
            self.status == "ACTIVE",
        )

    def __repr__(self):
        return f"LoanLender(id: {self.id}, contribution={self.amount_contributed})"


class LoanAgreement:
    def __init__(self):
        pass

    def create(loan_id, borrower, agreement_date, lenders):
        t = LoanAgreement()
        t.loan_id = loan_id
        t.borrower = borrower
        t.agreement_date = datetime(agreement_date)
        t.lenders = lenders
        return t

    def deserialize(mongo_agreement):
        try:
            t = LoanAgreement()
            t.loan_id = mongo_agreement["loan_id"]
            t.borrower = UUID(bytes=mongo_agreement["borrower"])
            t.agreement_date = mongo_agreement["agreement_date"]
            #
            t.lenders = []
            for l in mongo_agreement["lenders"]:
                lender = LoanLender(l)
                lender.add_amount_received("1.11")
                t.lenders.append(lender)
                return t
        except:
            raise Exception("LoanAgreement: deserialization failed {}", mongo_agreement)

    def to_pretty_str(self):
        return (
            "\t(_id: {},\n\t date: {},\n\t borrower_id: {}, \n\t lenders: {}, )".format(
                self.loan_id,
                self.loan_id,
                str(self.agreement_date),
                self.borrower,
                self.lenders,
            )
        )

    def __str__(self):
        return "(_id: {},loan_id: {},agreement_date: {},borrower_id: {},lenders: {})".format(
            self.loan_id,
            self.loan_id,
            str(self.agreement_date),
            self.borrower,
            self.lenders,
        )

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "borrower": self.borrower,
            "lenders": self.lenders,
            "agreement_date": self.agreement_date,
        }


def test_get_loan_agreement(kdb):
    agreement = kdb.get_loan_agreement(251000400)
    # print(agreement)
    loan_agreement = LoanAgreement.deserialize(agreement)
    ## TODO: add asserts
    print(loan_agreement)


def test_create_loan_agreement(kdb):
    agreement = kdb.get_loan_agreement(251000400)
    loan_agreement = LoanAgreement.deserialize(agreement)
    loan_agreement.loan_id = 259000999
    loan_agreement.borrower_id = "540b39ee-f53b-4723-af4f-65353a62265d"
    kdb.create_new_loan_agreement(loan_agreement)
    logger.error("Trying to print")
    print(loan_agreement)


def test_get_loan_agreements(kdb):
    agreements = kdb.get_loan_agreements().find({})
    loan_agreements = []
    for agreement in agreements:
        loan_agreement = LoanAgreement.deserialize(agreement)
        loan_agreements.append(loan_agreement)
    ## TODO: add asserts
    for loan_agreement in loan_agreements:
        print(loan_agreement)


def main():
    ##
    try:
        kdb = KoinDB("mongodb://localhost", 27017)
        ###
        if kdb.haveKoinDB():
            test_get_loan_agreements(kdb)
            test_get_loan_agreement(kdb)
            # test_create_loan_agreement(kdb)
        else:
            logger.error("koinDB not found!\n")
        ###
        kdb.close()
    except Exception as err:
        logger.error(err)
    ##
    logging.shutdown()


if __name__ == "__main__":
    init_logger("__koindb__")
    main()
