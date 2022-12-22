CREATE TABLE IF NOT EXISTS guild.logs
(
    id bigint NOT NULL DEFAULT nextval('guild.logs_id_seq'::regclass),
    chat_id bigint,
    exception_name character varying COLLATE pg_catalog."default",
    exception_desc character varying COLLATE pg_catalog."default",
    exception_code bigint,
    "timestamp" timestamp with time zone DEFAULT now(),
    CONSTRAINT logs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.logs
    OWNER to postgres;