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
	FROM guild.users gu
    INNER JOIN guild.users_roles gur ON gu.id = gur.user_id
    INNER JOIN guild.roles gr ON gur.role_id = gr.id
	WHERE gu.telegram_id = v_telegram_id and gr.name = "STAFF"
);
END;
$BODY$;

ALTER FUNCTION guild.telegram_id_staff_check()
    OWNER TO postgres;
