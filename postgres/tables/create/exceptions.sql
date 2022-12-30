CREATE TABLE IF NOT EXISTS guild.exceptions
(
    id bigint NOT NULL DEFAULT nextval('guild."errors.sql_id_seq"'::regclass),
    chat_id bigint NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default" NOT NULL,
    code bigint NOT NULL,
    "timestamp" timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT "errors.sql_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.exceptions
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_errors_id
    ON guild.exceptions USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;