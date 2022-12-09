CREATE OR REPLACE FUNCTION guild.telegram_id_staff_check(
		v_telegram_id bigint
	)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
BEGIN    
RETURN QUERY (
	SELECT COUNT(*) = 1
	FROM guild.users
	WHERE is_staff = TRUE and telegram_id = v_telegram_id
);
END;
$BODY$;

ALTER FUNCTION guild.telegram_id_staff_get()
    OWNER TO postgres;
