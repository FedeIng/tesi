CREATE TABLE IF NOT EXISTS guild.users_roles
(
    user_id bigint NOT NULL,
    role_id bigint NOT NULL,
    CONSTRAINT users_roles_pkey PRIMARY KEY (user_id,role_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.users_roles
    OWNER to postgres;