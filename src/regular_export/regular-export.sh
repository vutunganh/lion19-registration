#!/usr/bin/env sh

set -eu

date=`date +%Y-%m-%d_%H:%M:%S`
daily_name=/tmp/lion19_daily_export_"$date".csv
complete_name=/tmp/lion19_complete_export_"$date".csv

last_update="`psql -c 'COPY(SELECT MAX(ts) FROM participant_export_ts) TO STDOUT'`"
psql -c "INSERT INTO participant_export_ts VALUES (CURRENT_TIMESTAMP)"

psql -f query_for_daily.sql > "$daily_name"
psql -f query_for_complete.sql > "$complete_name"

translate_bool_to_czech() {
  file_name="$1"
  sed -i -s 's|;t;|;ano;|g' "$file_name"
  sed -i -s 's|;t$|;ano|g' "$file_name"
  sed -i -s 's|;f;|;ne;|g' "$file_name"
  sed -i -s 's|;f$|;ne|g' "$file_name"
}
translate_bool_to_czech "$daily_name"
translate_bool_to_czech "$complete_name"

prepend_bom_sequence() {
  file_name="$1"
  tmp_file_name="$file_name.tmp"
  mv "$file_name" "$tmp_file_name"
  printf '\357\273\277' > "$file_name"
  cat "$tmp_file_name" >> "$file_name"
  rm "$tmp_file_name"
}
prepend_bom_sequence "$daily_name"
prepend_bom_sequence "$complete_name"

for e in $EMAIL_ADDRESSES; do
  mutt -s "[LION19] Denni export (naposledy proveden '$last_update')" -a "$daily_name" -a "$complete_name" -- "$e" <<EOF
Ahoj, Petro a ostatni,

v priloze posilam exportovane seznamy ucastniku ve formatu csv. Exporty jsou dva:
  1. vyexportovany seznam ucastniku od minule. Naposledy byl export proveden '$last_update'.
    * Jmenuje se '`basename $daily_name`'.
  2. Celkovy seznam ucastniku.
    * Jmenuje se '`basename $complete_name`'.

Zdravim
  Tung

Tohle je automaticky email. Mate-li podezreni, ze je neco zle, napiste mi (<tung@iuuk.mff.cuni.cz>).
EOF
done
