
# Read Isolation, Consistency, and Recency
https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/


###  Causal Consistency Guarantees:

- If an operation A causally precedes another operation B, then all nodes that observe B must also observe A.

- Concurrent operations (those that are not causally related) can be seen in different orders on different replicas.

Effect of Network Partitions:

- In the event of a partition, different groups of replicas might diverge because they cannot see updates from each other.
- When the partition is resolved, merging updates while maintaining causal order can be complex, and some reconciliation may be needed.

Comparison to Strong Consistency:

- Unlike strong consistency (such as linearizability), causal consistency does not enforce a single global order of all operations.
- This means that different replicas can temporarily diverge during a partition.

- Thus, while causal consistency preserves "happens-before" relationships, it does not ensure that all replicas will always be in sync, especially under network partitions.


### Causal Consistency Guarantees
- https://www.mongodb.com/docs/manual/core/read-isolation-consistency-recency/#causal-consistency-guarantees

- The causal consistency guarantees provided by causally consistent sessions for
    - read operations with "majority" read concern and
    - write operations with "majority" write concern.


### Guarantees  Description
- **Read your writes**
    - Read operations reflect the results of write operations that precede them.

- **Monotonic reads**
    - Read operations do not return results that correspond to an earlier state of the data than a preceding read operation.
```
    If in a session:
    write 1 precedes write 2,

    read 1 precedes read 2, and

    read 1 returns results that reflect write 2

    then read 2 cannot return results of write 1.
```

- **Monotonic writes**
    - Write operations that must precede other writes are executed before those other writes.
```
    If write 1 must precede write 2 in a session,
    the state of the data at the time of write 2 must reflect
    the state of the data post write 1.

    Other writes can interleave between write 1 and write write 2,
    but write 2 cannot occur before write 1.
```

- **Writes follow reads**
    - Write operations that must occur after read operations are executed after those read operations.
        - That is, the state of the data at the time of the write must incorporate the state of the data of the preceding read operations.