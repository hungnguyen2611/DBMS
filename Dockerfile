FROM mcr.microsoft.com/mssql/server:2022-latest
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Playluv1@
ENV MSSQL_PID=Developer
ENV MSSQL_TCP_PORT=1433

WORKDIR /src

COPY scripts.sql ./scripts.sql
COPY generated/Book.sql ./Book.sql
COPY generated/Author.sql ./Author.sql
COPY generated/Genre.sql ./Genre.sql
COPY generated/BookGenre.sql ./BookGenre.sql


RUN (/opt/mssql/bin/sqlservr --accept-eula & ) | grep -q "MSSQL has started" &&  /opt/mssql-tools/bin/sqlcmd -S127.0.0.1 -Usa -PPlayluv1@ -i scripts.sql