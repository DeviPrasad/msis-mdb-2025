MongoDB - mongosh Methods

https://www.mongodb.com/docs/manual/reference/method/

https://www.mongodb.com/docs/manual/reference/method/#connection
https://www.mongodb.com/docs/manual/tutorial/query-documents/

show dbs

use koinDB
db.dropDatabase()

let koin = db.getMongo().startSession({ retryWrites: true, causalConsistency: true }).getDatabase("koinDB");
koin.getCollectionNames()


koin.loan_purpose_master.drop()
koin.createCollection("loan_purpose_master")
koin.getCollectionInfos()

koin.loan_purpose_master.insertMany([
    { _id: "farming", desc: "Farming loan", active: true, startDate: Date("2025-01-01") },
    { _id: "livestock", desc: "Livestock loan", active: true },
    { _id: "retail_store", desc: "Loan for a retail-store business", active: true },
    { _id: "eco_farming", desc: "Loan for organic and eco-friendly farming", active: true },
    { _id: "AHD", desc: "Animal Husbandry and Dairy", active: true, effectiveDate: {} },
    { _id: "education", desc: "Education loan for school/college/university education", active: true },
    { _id: "energy", desc: "Loans for innovative energy businesses", active: true },
    { _id: "artisan", desc: "Artisan fund", active: false, },
])
koin.getCollectionInfos()

let purpose_view = koin.createView('purpose_master_view', 'loan_purpose_master', [])
koin.getCollectionInfos()


koin.loan_purpose_master.find()

koin.loan_purpose_param.drop()
koin.createCollection("loan_purpose_param", {
    validator: {
        $jsonSchema: {
            required: ["purposeId", "rateOfInterest"],
            properties: {
                purposeId: {
                    bsonType: "string"
                },
                rateOfInterest: {
                    bsonType: "double",
                    minimum: 8,
                    maximum: 20,
                },
                effectiveDate: {
                    bsonType: "object",
                    required: ["startDate"],
                    properties: {
                        startDate: {
                            bsonType: "date",
                        },
                        endDate: {
                            bsonType: "date",
                        }
                    }
                },
            }
        }
    }
})


koin.loan_purpose_param.insertMany([
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "education" })._id,
        rateOfInterest: 11.5,
        effectiveDate: {
            startDate: new Date("2024-01-01")
        }
    },
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "farming" })._id,
        rateOfInterest: 8,
        effectiveDate: {
            startDate: new Date("2024-06-01")
        }
    },
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "retail_store" })._id,
        rateOfInterest: 14,
        effectiveDate: {
            startDate: new Date("2022-01-01")
        }
    },
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "AHD" })._id,
        rateOfInterest: 10,
        effectiveDate: {
            startDate: new Date("2023-06-01")
        }
    },
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "farming" })._id,
        rateOfInterest: 9,
        effectiveDate: {
            startDate: new Date("2024-08-01")
        }
    },
    {
        purposeId: db.loan_purpose_master.findOne({ _id: "education" })._id,
        rateOfInterest: 12,
        effectiveDate: {
            startDate: new Date("2025-01-01")
        }
    },
])

koin.loan_purpose_param.estimatedDocumentCount()
koin.loan_purpose_param.countDocuments()



koin.loan_agreements.drop()
koin.createCollection("loan_agreements", {
    validator: {
        $jsonSchema: {
            required: ["loan_id", "lenders", "borrower", "agreement_date"],
            properties: {
                loan_id: {
                    bsonType: "int",
                    minimum: 240000001,
                    maximum: 279999999
                },
                lenders: {
                    bsonType: "array",
                    minItems: 1,
                    maxItems: 8, // demonstrate its validation by reducing this number to 1
                    uniqueItems: true, // demonstrate its validation by duplicating an 'id'
                    additionalProperties: false,
                    items: {
                        bsonType: ["object"],
                        required: ["id", "amount_contributed", "disbursed", "status", "amount_received"],
                        additionalProperties: false,
                        properties: {
                            id: {
                                bsonType: "binData" // notice binary data
                            },
                            amount_contributed: {
                                bsonType: "int",
                                minimum: 2000,
                            },
                            disbursed: {
                                bsonType: "bool"
                            },
                            status: {
                                enum: ['active', 'closed', 'on_hold'],
                            },
                            amount_received: {
                                bsonType: "decimal"
                            }
                        }
                    }
                },
                borrower: {
                    bsonType: "binData"
                },
                agreement_date: {
                    bsonType: "date"
                }
            }
        }
    }
})

koin.getCollectionInfos()
koin.getCollectionInfos({ name: 'loan_agreements' })


koin.loan_agreements.deleteMany({})

koin.loan_agreements.insertOne({
    _id: 250000050,
    loan_id: 250000050,
    lenders: [
        {
            id: UUID('422ed138-9013-45a8-a349-b5101a498362'),
            amount_contributed: 10000,
            disbursed: true,
            status: "active",
            amount_received: NumberDecimal('1000.80')
        }
    ],
    borrower: UUID('e97e3c8a-3972-4f07-bc43-e1e21e7f8244'),
    agreement_date: new Date("2024-03-10T15:30:10.234Z")
})

koin.loan_agreements.countDocuments()

koin.loan_agreements.insertMany([
    {
        _id: 250000100,
        loan_id: 250000100,
        lenders: [
            {
                id: UUID('a86620b7-5d47-49a2-a45e-237ffcce5987'),
                amount_contributed: 7300,
                disbursed: true,
                status: "active",
                amount_received: NumberDecimal('545.17')
            },
            {
                id: UUID('613ec765-a62d-40b7-a42e-f8246203594a'),
                amount_contributed: 5200,
                disbursed: true,
                status: "active",
                amount_received: NumberDecimal('300')
            },
            {
                id: UUID('dca9e2cd-ffe2-4010-b3cd-15e130deb087'),
                amount_contributed: 10000,
                disbursed: true,
                status: "active",
                amount_received: NumberDecimal('3250.68')
            }
        ],
        borrower: UUID('b5f13225-15c8-4ed2-a2f3-a8fa26c90df3'),
        agreement_date: new Date("2024-11-20T15:30:10.234Z")
    },

    {
        _id: 250000302,
        loan_id: 250000302,
        lenders: [
            {
                id: UUID('613ec765-a62d-40b7-a42e-f8246203594a'),
                amount_contributed: 10000,
                disbursed: true,
                status: "closed",
                amount_received: NumberDecimal('7310.80')
            }
        ],
        borrower: UUID('b5f13225-15c8-4ed2-a2f3-a8fa26c90df3'),
        agreement_date: new Date("2024-11-20T15:30:10.234Z")
    },

    {
        _id: 251000400,
        loan_id: 251000400,
        lenders: [
            {
                id: UUID('dca9e2cd-ffe2-4010-b3cd-15e130deb087'),
                amount_contributed: 25000,
                disbursed: false,
                status: "on_hold",
                amount_received: NumberDecimal('0')
            }
        ],
        borrower: UUID('b5f13225-15c8-4ed2-a2f3-a8fa26c90df3'),
        agreement_date: new Date("2024-11-20T15:30:10.234Z")
    },
])

koin.loan_agreements.find({})
koin.loan_agreements.estimatedDocumentCount()
koin.loan_agreements.countDocuments()



kdb.loan_accounts.drop()
kdb.createCollection("loan_accounts", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            title: "Loan Account Entry Validation",
            required: ["LoanId", "accId", "loanAmount", "tenor", "rateOfInterest", "status", "openedDate"],
            properties: {
                loanId: {
                    bsonType: "string",
                    maxLength: 36,
                    minLength: 36,
                    description: "unique loan id stored as a uuid"
                },
                accId: {
                    bsonType: "string",
                    maxLength: 14,
                    minLength: 14,
                    description: "unique loan account number"
                },
                borrowers: {},
                lenders: {},
                loanAmount: {
                    bsonType: "long",
                    minimum: 5000,
                    maximum: 1000000,
                },
                tenor: {
                    bsonType: "long",
                    minimum: 12,
                    maximum: 48,
                    description: "loan period in months"
                },
                rateOfInterest: {
                    bsonType: "long",
                    minimum: 1,
                    maximum: 10,
                    description: "rate of interest ranges from 1% to 10%"
                },
                status: {
                    enum: ['active', 'closed', 'written-off', 'dormant'],
                    description: "current state of the account"
                },
                openedDate: {
                    bsonType: "date",
                },
                closedDate: {
                    bsonType: "date",
                },
                lastStatusModDate: {
                    bsonType: "date",
                },
            }
        }
    }
})


function getLoanPurposeParamForRate(appDB, rate) {
    let params = [];

    const cursor = appDB.loan_purpose_param.find();
    while (cursor.hasNext()) {
        const p = cursor.next();
        if (p.rateOfInterest >= rate) {
            params.push({
                id: p.purposeId,
                rateOfInterest: p.rateOfInterest
            }
            );
        }
    }
    return params;
}

function getLoanPurposeParamForRate(appDB, rate) {
    let params = [];

    const cursor = appDB.loan_purpose_param.find({ rateOfInterest: { $gte: rate } });
    while (cursor.hasNext()) {
        const p = cursor.next();
        params.push({
            id: p.purposeId,
            rateOfInterest: p.rateOfInterest
        }
        );
    }
    return params;
}

function getLoanPurposeParamForRateSorted(appDB, purposeId, rate) {
    let params = [];

    const cursor = appDB.loan_purpose_param.find({
        purposeId: purposeId,
        rateOfInterest: { $gte: rate }
    })
        .sort({ rateOfInterest: -1, "effectiveDate.startDate": -1 })
        .limit(3);

    while (cursor.hasNext()) {
        const p = cursor.next();
        params.push({
            id: p.purposeId,
            rateOfInterest: p.rateOfInterest,
            startDate: p.effectiveDate.startDate
        }
        );
    }
    return params;
}

getLoanPurposeParamForRateSorted(koin, "education", 7)
