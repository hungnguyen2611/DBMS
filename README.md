# Data ingestion
## Generate SQL scripts to ingesting CSV file
### Prerequisites
```bash
pip install pandas click
```
## Generate
- Generator will be create a sql file according sheet name
```bash
python sql_generator.py --generate /data/<filename>.xlsx --outputdir ./generated/
```
Ref: [here](https://blog.piinalpin.com/2020/12/sql-generator/)
## Build Docker Image for MSSQL

```bash
sudo docker build -t mcr.microsoft.com/mssql/server:2022-latest -f Dockerfile .
```
- Run
```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=Playluv1@" -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
```
- Execute
```bash
docker exec -it <CONTAINER_ID> /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Playluv1@
```


# API 
Moving to [api](/api)
## Prerequisites
For API service
```bash
pip install fastapi "uvicorn[standard]"
```
Ref: [here](https://fastapi.tiangolo.com/)
For MSSQL connection
```bash
pip install python-tds
```
Ref: [here](https://github.com/denisenkom/pytds)
- Run as localhost
```bash
uvicorn main:app --reload
```

DB Credential infos:
- Host: `localhost`
- Port: `1433`
- Database name: `master`
- Username: `sa`
- Pass: `Playluv1@`




