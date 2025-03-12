# Vector Similarity Search for Postgres

Postgres Extension
- https://github.com/pgvector/pgvector

pgvector support for Python
- https://github.com/pgvector/pgvector-python

An Example
- https://github.com/pgvector/pgvector-python/blob/master/examples/openai/example.py

Distance Metrics
- https://weaviate.io/blog/distance-metrics-in-vector-search



## Admin
```sql

$ psql -U postgres
pg> create role msismdb login password 'admin123' ;
pg> create database vector with owner = msismdb;

pg> create role dba with SUPERUSER;
pg> grant dba to msismdb;



```



## User

```sql
$ psql -d vector -U msismdb
pg> set role dba;

pg> create extension vector;
pg> \du

pg> create table items (id bigserial primary key, embedding vector(3));

pg>

pg>
pg>
pg>
pg>
pg>
pg>
pg>
pg>
pg>

```


```python

import psycopg2
import pgvector

conn = psycopg2.connect(host='localhost', port='5432', database='vector', user='msismdb')
cursor = conn.cursor()

pg_res = cursor.execute("select * from items")

# result set
rs = cursor.fetchall()

cursor.close()
conn.close()

```

```python

import psycopg2
import pgvector
from pgvector.psycopg2 import register_vector
conn = psycopg2.connect(host='localhost', port='5432', database='vector', user='msismdb')
cursor = conn.cursor()
cursor.execute('CREATE EXTENSION IF NOT EXISTS vector')
register_vector(conn)

# enable autocommit
conn.autocommit = True


```