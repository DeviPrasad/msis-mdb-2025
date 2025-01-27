### Reference - Relational Data Model
- Designing Data-Intensive Applications - Martin Kleppmann.
- Chapter 2: Data Models and Query Languages, pages 38-42
- Relational Versus Document Databases Today

### Reference - Document Data Model

### Relational Data Model
- Relation is the basic concept - the **primitive**
- Everything is a Relation
- A database is a set of relations

<br>

### Document Data Model
- A *Document* is the primitive concept
- Everything is a Document
- A collection is set of document

<br><br>


### What is a Document Database?
https://www.mongodb.com/resources/basics/databases/document-databases

Document databases offer a variety of advantages, including:
- An intuitive data model that is fast and easy for developers to work with.
- A flexible schema that allows for the data model to evolve as application needs change.
- The ability to horizontally scale out.

<br><br>


### MongoDB Schema Design - Data Modeling Best Practices
https://www.mongodb.com/developer/products/mongodb/mongodb-schema-design-best-practices/
    - Updated Oct 02, 2024

With MongoDB schema design, there is:
- No formal process
- No algorithms
- No rules

<br><br>

### Example 1

#### Paddle
- https://developer.paddle.com/api-reference/
- Products
- Discounts
- Customer

<br><br>
### Example 2

#### Digilocker
- https://docs.setu.co/data/digilocker/api-reference#/operation~Gete-AadhaarXML


<br><br>


### MongoDB - Embedding vs. Referencing

#### Embedding Advantages
- You can retrieve all relevant information in a single query.
- Avoid implementing joins in application code or using **$lookup**.
- Update related information as a single atomic operation.
- By default, all CRUD operations on a single document are ACID compliant.
- However, if you need a transaction across multiple operations, you can use the transaction operator.
    - transactions are available starting 4.0
    - it's an anti-pattern to be overly reliant on using them in your application.

#### Embedding Limitations
- Large documents mean more overhead if most fields are not relevant.
- You can increase query performance by limiting the size of the documents that you are sending over the wire for each query.
- There is a 16-MB document size limit in MongoDB
- If you are embedding too much data inside a single document, you could potentially hit this limit.


#### Referencing Advantages
- By splitting up data, you will have smaller documents.
- Less likely to reach 16-MB-per-document limit
- Infrequently accessed information not needed on every query.
- Reduce the amount of duplication of data.
    - data duplication should not be avoided if it results in a better schema.

#### Limitations
- to retrieve all the data in the referenced documents, a minimum of two **$lookup** are required.