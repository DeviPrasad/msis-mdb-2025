
### Session A

mysql --user 'mdb_py_script' -p'{MdbPyScript!!2025/01/*}' --host 'multicore.in' --port 41526 -D'mdb_intro'

set autocommit = 0;

set transaction isolation level serializable;
start transaction;

select b from t for update;
update t set b = b + 100;

commit;

select b from t;



### Session B

mysql --user 'mdb_py_script' -p'{MdbPyScript!!2025/01/*}' --host 'multicore.in' --port 41526 -D'mdb_intro'

set autocommit = 0;

set transaction isolation level serializable;
start transaction;

update t set b=b+5;

rollback;




