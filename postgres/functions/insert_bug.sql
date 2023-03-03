CREATE OR REPLACE FUNCTION guild.insert_bug(
	v_chat_id bigint,
    v_bot_name character varying,
	v_bug_desc character varying)
    RETURNS TABLE(result boolean) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
DECLARE
	t_count bigint;
BEGIN    
SELECT COUNT(*) INTO t_count
FROM guild.bugs
WHERE chat_id = v_chat_id and bot_name = v_bot_name and description = v_bug_desc;
INSERT INTO guild.bugs(chat_id, bot_name, description)
	VALUES (v_chat_id, v_bot_name, v_bug_desc);
RETURN QUERY (
	SELECT COUNT(*) = t_count + 1
	FROM guild.bugs
	WHERE chat_id = v_chat_id and bot_name = v_bot_name and description = v_bug_desc
);
END;
$BODY$;

ALTER FUNCTION guild.insert_bug(bigint, character varying, character varying)
    OWNER TO postgres;