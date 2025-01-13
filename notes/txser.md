

## Write-ahead Log (WAL)

Idea

-  append only and _immutable_ data structure
- Inherently sequential
- readers can safely access till the last write threshold

Contents

- Every record has a unique, monotonically increasing log sequence number (LSN)
- LSN may be an internal counter or a timestamp
- _commit_ records mark the transaction being committed
- very tricky to engineer it correctly

Checkpoint
- Checkpoints fully persist log records
- log records are not required beyond a checkpoint
- this significantly reduces the amount of work required during the database startup
- sync checkpoint fully synchronizes the primary storage structure




## Serializability


### SQL Standard Isolation Levels
- Serializable
    - no dirty read
    - no non-repeatable read
    - no phantom read
- Repeatable read
    - default isolation level in MySQL
    - no dirty read
    - no non-repeatable read
    - phantom read is possible
- Read committed
    - default isolation level in PostgreSQL
    - no dirty read
    - possible non-repeatable read
    - phantom read is not possible
- Read uncommitted
    - allows dirty read
    - allows non-repeatable read
        - reads data written by a concurrent uncommitted transaction.
    - allows phantom read


### PostgreSQL Transaction Isolation
- https://www.postgresql.org/docs/current/transaction-iso.html
