CREATE TABLE IF NOT EXISTS guild.bugs
(
    id bigint NOT NULL DEFAULT nextval('guild.bugs_id_seq'::regclass),
    chat_id bigint,
    bot_name character varying COLLATE pg_catalog."default",
    "description" character varying COLLATE pg_catalog."default",
    "timestamp" timestamp with time zone DEFAULT now(),
    CONSTRAINT bugs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.bugs
    OWNER to postgres;