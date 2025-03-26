

A partition occurs when a primary goes down. The primary is unavailable till a new one is elected.

A partition cal also occur when the primary looses connection with the secondaries. Once again, the secondaries will elect a new primary.

MongoDB favors consistency over availability in the face of a partition.


https://www.mongodb.com/community/forums/t/does-query-advance-logical-time-in-mongodb/7712/3
- You are node 1. You think it’s T1. Meanwhile node 2 has taken several writes advancing the cluster time to T3. Next request, no matter what it is to node 1 will notify node 1 that the current cluster time is T3 not T1. That does not advance the cluster clock that just catches up node 1 which was snoozing and didn’t realize that the cluster time has advanced.

- There is no such thing as multiple cluster times. There is one. Not all nodes/clients may realize where it is at a particular point and they can learn about it with any communication even one that doesn’t involve any query.


hybrid logical clocks (HLCs) and gossiping
- https://dl.acm.org/doi/pdf/10.1145/3299869.3314049


https://en.wikipedia.org/wiki/CAP_theorem

Consistency
- Every read receives the most recent write or an error. Note that consistency as defined in the CAP theorem is quite different from the consistency guaranteed in ACID database transactions.[4]

Availability
- Every request received by a non-failing node in the system must result in a response. This is the definition of availability in CAP theorem as defined by Gilbert and Lynch.[1] Note that availability as defined in CAP theorem is different from high availability in software architecture.[5]

Partition tolerance
- The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

When a network partition failure happens, it must be decided whether to do one of the following:
- cancel the operation and thus decrease the availability but ensure consistency
- proceed with the operation and thus provide availability but risk inconsistency.
- Note this doesn't necessarily mean that system is highly available to its users.