CREATE TYPE participant_type AS ENUM ('REGULAR', 'STUDENT', 'ACCOMPANYING');

CREATE TABLE IF NOT EXISTS participant (
  id                                SERIAL           PRIMARY KEY,

  full_name                         VARCHAR(512)     NOT NULL,
  affiliation                       VARCHAR(256),
  email                             VARCHAR(512)     NOT NULL,

  invoicing_address_line_1          VARCHAR(256)     NOT NULL,
  invoicing_address_line_2          VARCHAR(256),
  invoicing_address_city            VARCHAR(256),
  invoicing_address_country         VARCHAR(256)     NOT NULL,
  invoicing_address_zip_code        VARCHAR(64),
  invoicing_vat_number              VARCHAR(64),

  participant_type                  participant_type NOT NULL,

  remarks                           VARCHAR(16384),

  date_registered                   TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP
);
