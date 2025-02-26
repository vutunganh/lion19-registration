CREATE EXTENSION fuzzystrmatch;

CREATE TYPE registration_fee_type AS ENUM ('FULL', 'DISCOUNTED', 'STUDENT');

CREATE TABLE IF NOT EXISTS participant (
  id                     SERIAL                PRIMARY KEY,

  postal_mail_opt_out    BOOLEAN               NOT NULL,
  email_opt_in           BOOLEAN               NOT NULL,

  full_name              VARCHAR(512)          NOT NULL,
  affiliation            VARCHAR(256),
  email                  VARCHAR(256)          NOT NULL,

  acm_membership_number  VARCHAR(64),
  ieee_membership_number VARCHAR(64),
  is_student             BOOLEAN               NOT NULL DEFAULT FALSE,
  fee_type               registration_fee_type NOT NULL,

  remarks                VARCHAR(16384),

  date_registered        TIMESTAMP             NOT NULL DEFAULT CURRENT_TIMESTAMP
);
