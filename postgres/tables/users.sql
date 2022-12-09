CREATE TABLE IF NOT EXISTS guild.users
(
    id bigint NOT NULL DEFAULT nextval('guild.users_id_seq'::regclass),
    telegram_id bigint,
    telephone character varying COLLATE pg_catalog."default",
    name character varying COLLATE pg_catalog."default",
    surname character varying COLLATE pg_catalog."default",
    nickname character varying COLLATE pg_catalog."default",
    is_staff boolean DEFAULT false,
    CONSTRAINT users_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.users
    OWNER to postgres;