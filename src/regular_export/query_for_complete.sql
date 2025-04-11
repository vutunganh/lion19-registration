COPY (
    SELECT *
    FROM participant
    ORDER BY email, date_registered DESC
)
TO STDOUT WITH DELIMITER ';';
