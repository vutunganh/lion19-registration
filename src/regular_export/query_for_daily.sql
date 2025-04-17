COPY (
    SELECT *
    FROM participant
    WHERE date_registered >= (
        SELECT ts
        FROM participant_export_ts
        ORDER BY ts DESC
        OFFSET 1 LIMIT 1
    )
    AND date_registered < (
        SELECT MAX(ts)
        FROM participant_export_ts
    )
    ORDER BY email, date_registered DESC
)
TO STDOUT WITH CSV HEADER DELIMITER ';';
