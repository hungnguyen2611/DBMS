#!/bin/sh
echo -e "$(date +%F\ %T.%N) \t SQL Server entrypoint..."
/opt/mssql/bin/sqlservr &
sleep 10

echo -e "$(date +%F\ %T.%N) \t Database server has started, creating database"
for i in scripts.sql Author.sql Book.sql Genre.sql BookGenre.sql
do
  /opt/mssql-tools/bin/sqlcmd -S 127.0.0.1 -U sa -P Playluv1@ -d master -i $i
  echo -e "execute $i done"
  sleep 5
done