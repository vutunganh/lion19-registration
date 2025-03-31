ALTER TABLE participant
ADD COLUMN photo_consent BOOLEAN;

UPDATE participant
SET photo_consent = false;

ALTER TABLE participant
ALTER COLUMN photo_consent SET NOT NULL;
