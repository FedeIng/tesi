CREATE TABLE IF NOT EXISTS guild.users_games
(
    id bigint NOT NULL DEFAULT nextval('guild.users_games_id_seq'::regclass),
    user_id bigint NOT NULL,
    game_id bigint NOT NULL,
    staff_id bigint,
    lending_ts timestamp with time zone NOT NULL DEFAULT now(),
    restitution_ts timestamp with time zone,
    CONSTRAINT users_games_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS guild.users_games
    OWNER to postgres;