
REVOKE ALL PRIVILEGES, GRANT OPTION  FROM 'mdb_py_script'@'multicore.in';

REVOKE INSERT ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE UPDATE ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE TRUNCATE ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE ALTER ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE DELETE ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE DROP ON *.* FROM 'mdb_py_script'@'multicore.in';
REVOKE SHUTDOWN ON *.* FROM 'mdb_py_script'@'multicore.in';


GRANT SELECT, SHOW VIEW, PROCESS ON *.* TO 'mdb_py_script'@'multicore.in';
GRANT CREATE TEMPORARY TABLES ON *.* TO 'mdb_py_script'@'multicore.in';

GRANT INSERT ON *.* TO 'mdb_py_script'@'multicore.in';

flush privileges;
