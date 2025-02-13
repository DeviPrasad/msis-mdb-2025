
# Replication and Sharding

Large data sets and high-throughput requirements necessitate replication and sharding.

sharding is a practical when apps frequently access large legacy data sets.


### MongoDB documentation about replication and sharding
- https://www.mongodb.com/docs/manual/replication/
- https://www.mongodb.com/docs/manual/sharding/


### MongoDB Blog - How does replication work in MongoDB?
- https://www.mongodb.com/resources/products/capabilities/replication

## MongoDB Replica set
- https://www.mongodb.com/docs/manual/replication/#replication-in-mongodb

### Replication
- maintains multiple copies of the same data across database servers
- improves
  - data availability
  - fault-tolerance
  - data locality
  - reporting
  - backups
  - disaster recovery


### A replica set is a
- group of **mongod** processes that maintain the *same* data set
- one primary node
- multiple secondary nodes
- an arbiter node

### When the primary node dies
- replica set turns read-only
- any attempt to write fails

### When the primary node dies
- may take tens of seconds before secondaries detect the condition

### When the primary node dies
- secondary nodes *elect* a new primary





## Sharding
- a method for distributing data across multiple machines
- deployments with very large data sets and high throughput requirements
- spread the system dataset and load across multiple servers
- *horizontal scaling*

## Sharding
- MongoDB shards data at the **collection** level
- distributes the collection data across shards in a cluster

### MongoDB Components
- mongod
    - https://www.mongodb.com/docs/manual/reference/program/mongod/
    - primary daemon process for the MongoDB system
    - handles data requests
    - manages data access
    - performs background management operations

- mongod replication options
    - https://www.mongodb.com/docs/manual/reference/program/mongod/#replication-options
- mongod sharding options
    - https://www.mongodb.com/docs/manual/reference/program/mongod/#sharded-cluster-options
- WiredTiger options
    - https://www.mongodb.com/docs/manual/reference/program/mongod/#wiredtiger-options

- Storage options
    - https://www.mongodb.com/docs/manual/reference/program/mongod/#storage-options


 - mogos
    - https://www.mongodb.com/docs/manual/reference/program/mongos/
    - interface between the client application and the sharded cluster
    - route queries and write operations to the shards



### Sharded Cluster
- https://www.mongodb.com/docs/manual/sharding/#sharded-cluster

### Shard Keys
- **shard key** is used to distribute a collection's documents across shards
- shard key consists of a field or multiple fields in the documents

### Shard Key Index
- To shard a populated collection, the collection must have an index
- The index must start with the shard key


### Sharded and Non-Sharded Collections
- https://www.mongodb.com/docs/manual/sharding/#sharded-and-non-sharded-collections
- Sharded collections are partitioned and distributed across shards in the cluster
- Unsharded collections can be located on any shard
    - cannot span across shards

### Connecting to a Sharded Cluster
- must connect to a mongos router to interact with any collection in the sharded cluster
- connect to a mongos the same way you connect to a mongod
    - mongosh
    - MongoDB driver

### Sharding Strategy
- Ranged sharding
    - range of shard keys whose values are "close" are more likely to reside on the same chunk
    - has tendency to create target operations

- Hashed sharding
    - a chunk is then assigned a range based on the hashed shard key values
    - may result in more cluster wide broadcast operations
