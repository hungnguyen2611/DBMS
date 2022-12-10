import pytds
import uvicorn
from fastapi import FastAPI, HTTPException





class MSSQL:
    """MS SQL server instance"""
    def __init__(self, db_host:str, db_port:int, db_name:str, user_name:str, password:str) -> None:
        self.connection = None
        self.host = db_host
        self.port = db_port
        self.db_name = db_name
        self.user_name = user_name
        self.password = password
        self.is_connected = False

    def connect(self):
        self.connection = pytds.connect(
            dsn=self.host, 
            port=self.port, 
            database=self.db_name, 
            user=self.user_name, 
            password=self.password
        )
        self.is_connected=True
        return self.connection.cursor()

    def info(self):
        return {
            "host": self.host,
            "port": self.port,
            "database name": self.db_name,
            "user_name": self.user_name,
            "password": "********",
            "is connected?": self.is_connected
        }





app = FastAPI()
db = None

@app.get("/")
async def home():
    return {"message": "Head to http://127.0.0.1:8000/docs"}





@app.get("/connect")
async def connect_db(db_host, db_port, db_name, user, password):
    global db
    try:
        db = MSSQL(db_host, db_port, db_name, user, password)
        db.connect()
    except:
        raise HTTPException(status_code=503, detail="Can not connect to SQL Server")

    return {"message": "Connecting to SQL server successful!"}


@app.get("/info")
async def info():
    global db
    if db is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db.info()

@app.get("/query/")
async def query_rating(table: str, size: int, low:str, high:str):
    if db is None:
        return HTTPException(status_code=404, detail="Not found")
    cur = db.connection.cursor()
    try:
        cur.execute(f"SELECT TOP {size} * FROM {table} WHERE avg_rating BETWEEN {float(low)} AND {float(high)};")
    except:
        raise HTTPException(status_code=501, detail="The database isn't connected")
    data = cur.fetchall()
    return data



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)








        