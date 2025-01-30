MongoDB - mongosh Methods

https://www.mongodb.com/docs/manual/reference/method/

https://www.mongodb.com/docs/manual/reference/method/#connection
https://www.mongodb.com/docs/manual/tutorial/query-documents/

let koin = db.getMongo().startSession({ retryWrites: true, causalConsistency: true }).getDatabase("koinDB");

koin.loan_purpose_master.drop()
koin.createCollection("loan_purpose_master")

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
                    bsonType: "int",
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
        rateOfInterest: 12,
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
])

koin.loan_purpose_param.estimatedDocumentCount()
koin.loan_purpose_param.countDocuments()

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
        .limit(1);

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

getLoanPurposeParamForRateSorted(koin, "farming", 7)



kdb.accounts.drop()
kdb.createCollection("accounts", {
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
