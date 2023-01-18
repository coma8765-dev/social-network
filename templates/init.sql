create table public.users
(
    id            serial
        constraint users_pk
            primary key,
    email         varchar(100)            not null,
    password_hash varchar(60)             not null,
    email_confirm boolean   default false not null,
    create_date   timestamp default now() not null,
    name          varchar(60)
);

create unique index users_email_uindex
    on public.users (email);

create unique index users_id_uindex
    on public.users (id);

create table public.posts
(
    id          serial
        primary key,
    title       varchar(200)            not null,
    body        text                    not null,
    created_by  integer                 not null,
    create_date timestamp default now() not null
);

create table public.post_estimates
(
    id      serial
        primary key,
    post_id integer              not null
        constraint post_estimates_post_estimates_id_fk
            references public.posts
            on delete cascade,
    "like"  boolean default true not null,
    user_id integer              not null
        constraint post_estimates_users_id_fk
            references public.users
            on delete cascade
);

