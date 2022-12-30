CREATE TABLE IF NOT EXISTS guild.bugs
(
    id bigint NOT NULL DEFAULT nextval('guild.bugs_id_seq'::regclass),
    chat_id bigint NOT NULL,
    bot_name character varying COLLATE pg_catalog."default" NOT NULL,
    description character varying COLLATE pg_catalog."default" NOT NULL,
    "timestamp" timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT bugs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.bugs
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_bugs_id
    ON guild.bugs USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;