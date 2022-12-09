CREATE OR REPLACE FUNCTION guild.rental_get_by_telegram_id(
	v_telegram_id bigint)
    RETURNS TABLE(result character varying[]) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN
RETURN QUERY (SELECT ARRAY(SELECT gg.name
				from guild.users_games gug
			  	inner join guild.games gg on gug.game_id = gg.id
			  	inner join guild.users gu on gug.user_id = gu.id
				where gu.telegram_id = v_telegram_id and gug.restitution_ts IS NULL
			) as result);
END;
$BODY$;

ALTER FUNCTION guild.rental_get_by_telegram_id(bigint)
    OWNER TO postgres;