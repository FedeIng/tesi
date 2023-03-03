CREATE TABLE IF NOT EXISTS guild.roles
(
    id bigint NOT NULL,
    name character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT roles_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.roles
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_roles_id
    ON guild.roles USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;