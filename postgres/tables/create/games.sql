CREATE TABLE IF NOT EXISTS guild.games
(
    id bigint NOT NULL DEFAULT nextval('guild.games_id_seq'::regclass),
    name character varying COLLATE pg_catalog."default" NOT NULL,
    "number" smallint NOT NULL DEFAULT 1,
    CONSTRAINT games_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.games
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_games_id
    ON guild.games USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;