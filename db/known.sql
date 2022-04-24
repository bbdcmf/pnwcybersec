create table known
(
    file_hash  varchar(256)                 not null,
    label ENUM ('Malware', 'Goodware') not null,
    cnt   int default 0                not null,
    constraint known_pk
        primary key (file_hash)
);

create unique index known_file_hash_uindex
    on known (file_hash);
