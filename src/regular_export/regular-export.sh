#!/usr/bin/env sh

set -eu

date=`date +%Y-%m-%d_%H:%M:%S`
daily_name=/tmp/lion19_daily_export_"$date".csv
complete_name=/tmp/lion19_complete_export_"$date".csv

last_update="`psql -c 'COPY(SELECT MAX(ts) FROM participant_export_ts) TO STDOUT'`"
psql -c "INSERT INTO participant_export_ts VALUES (CURRENT_TIMESTAMP)"

psql -f query_for_daily.sql > "$daily_name"
psql -f query_for_complete.sql > "$complete_name"

for e in $EMAIL_ADDRESSES; do
  mutt -s "[LION19] Denni export (naposledy proveden '$last_update')" -a "$daily_name" -a "$complete_name" -- "$e" <<EOF
Ahoj, Petro a ostatni,

v priloze posilam exportovane seznamy ucastniku ve formatu csv. Exporty jsou dva:
  1. vyexportovany seznam ucastniku od vcerejska. Naposledy byl export proveden '$last_update'.
    * Jmenuje se '`basename $daily_name`'.
  2. Celkovy seznam ucastniku.
    * Jmenuje se '`basename $complete_name`'.

Zdravim
  Tung

Tohle je automaticky email. Mate-li podezreni, ze je neco zle, napiste mi (<tung@iuuk.mff.cuni.cz>).
EOF
done
