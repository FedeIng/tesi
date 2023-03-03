CREATE TABLE IF NOT EXISTS guild.users_roles
(
    user_id bigint NOT NULL,
    role_id bigint NOT NULL,
    CONSTRAINT users_roles_pkey PRIMARY KEY (user_id, role_id),
    CONSTRAINT role_pk FOREIGN KEY (role_id)
        REFERENCES guild.roles (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT user_id FOREIGN KEY (user_id)
        REFERENCES guild.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.users_roles
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_users_roles_role_id
    ON guild.users_roles USING btree
    (role_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_users_roles_user_id
    ON guild.users_roles USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;