FROM mcr.microsoft.com/mssql/server:2022-latest


ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Playluv1@
ENV MSSQL_PID=Developer
ENV MSSQL_TCP_PORT=1433

USER root
RUN apt-get update

WORKDIR /src

COPY scripts.sql ./scripts.sql
COPY generated/Book.sql ./Book.sql
COPY generated/Author.sql ./Author.sql
COPY generated/Genre.sql ./Genre.sql
COPY generated/BookGenre.sql ./BookGenre.sql
COPY run.sh ./run.sh


RUN chmod u+x ./run.sh
RUN ./run.sh