CREATE TABLE IF NOT EXISTS guild.users_games
(
    user_id bigint NOT NULL,
    game_id bigint NOT NULL,
    staff_id bigint,
    lending_ts timestamp with time zone NOT NULL DEFAULT now(),
    restitution_ts timestamp with time zone,
    id bigint NOT NULL DEFAULT nextval('guild.users_games_id_seq'::regclass),
    CONSTRAINT users_games_pkey PRIMARY KEY (id),
    CONSTRAINT game_pkey FOREIGN KEY (game_id)
        REFERENCES guild.games (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT user_pkey FOREIGN KEY (user_id)
        REFERENCES guild.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.users_games
    OWNER to postgres;

CREATE INDEX IF NOT EXISTS idx_users_games_game_id
    ON guild.users_games USING btree
    (game_id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_users_games_id
    ON guild.users_games USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;

CREATE INDEX IF NOT EXISTS idx_users_games_user_id
    ON guild.users_games USING btree
    (user_id ASC NULLS LAST)
    TABLESPACE pg_default;