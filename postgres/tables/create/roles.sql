CREATE TABLE IF NOT EXISTS guild.roles
(
    id bigint NOT NULL DEFAULT nextval('guild.roles_id_seq'::regclass),
    "name" character varying COLLATE pg_catalog."default",
    CONSTRAINT roles_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.roles
    OWNER to postgres;