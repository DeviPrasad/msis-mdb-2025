
create database mdb_intro;

create user 'mdb_py_script'@'multicore.in' identified by '{MdbPyScript!!2025/01/*}';
grant all privileges on mdb_intro.* to 'mdb_py_script'@'multicore.in' with grant option;
flush privileges;

$ mysql --user 'mdb_py_script' -p'{MdbPyScript!!2025/01/*}' --host 'multicore.in' --port 41526 -D'mdb_intro'

drop user 'mdb_py_script'@'multicore.in';


drop table if exists cust_neft_acc;
create table cust_neft_acc(
    cust_code         varchar(16),
    neft_acc          varchar(16),
    ifsc              char(11),
    status            enum("unverified", "ok", "error", "blocked", "removed") not null default "unverified",
    acc_holder_name   varchar(128),
    msg               varchar(128),
    cts               timestamp not null default current_timestamp,
    cuid              varchar(16) not null,

    primary key(cust_code, neft_acc),
    unique(neft_acc),
    index idx_cust_neft_acc_cc(cust_code)
);

insert into cust_neft_acc values('0914725006808325', '99305523040712', 'RXTC1740301', 'ok', 'Devi Prasad M', 'active account', default, 'MDB0025001267');
insert into cust_neft_acc values('0914725006808325', '14305523040802', 'RXTC1740301', 'ok', 'Devi Prasad M', 'active account', default, 'MDB0025001267');

delete from cust_neft_acc;

insert into cust_neft_acc values
    ('0914725006808325', '99305523040712', 'RXTC1740301', 'ok', 'Devi Prasad M', 'active account', default, 'MDB0025001267'),
    ('0945825006808325', '79305523040712', 'UNBC1740301', 'ok', 'Devi Prasad', 'active account', default, 'MDB0025001267'),
    ('0939825006808325', '14305523040802', 'SBI01740301', 'ok', 'Ravishankar S', 'active account', default, 'MDB0025001267');
