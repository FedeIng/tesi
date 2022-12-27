CREATE TABLE IF NOT EXISTS guild.exceptions
(
    id bigint NOT NULL DEFAULT nextval('guild.exceptions_id_seq'::regclass),
    chat_id bigint,
    "name" character varying COLLATE pg_catalog."default",
    "description" character varying COLLATE pg_catalog."default",
    code bigint,
    "timestamp" timestamp with time zone DEFAULT now(),
    CONSTRAINT exceptions_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.exceptions
    OWNER to postgres;