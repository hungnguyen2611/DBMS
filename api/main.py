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

@app.get("/query/book_rating")
async def query_book_rating(size: int, low:str, high:str, plan:int):
    if db is None:
        return HTTPException(status_code=404, detail="Not found")
    cur = db.connection.cursor()
    if plan == 1:
        cur.execute("SET SHOWPLAN_ALL ON")
    else:
        cur.execute("SET SHOWPLAN_ALL OFF")
    try:
        cur.execute(f"SELECT TOP {size} * FROM Book WHERE avg_rating BETWEEN {float(low)} AND {float(high)};")
    except:
        raise HTTPException(status_code=501, detail="The database isn't connected")
    data = cur.fetchall()
    data = {
        "_source": data
    }
    return data


@app.get("/query/name")
async def query_name(table: str, size: int, name: str, plan:int):
    if db is None:
        return HTTPException(status_code=404, detail="Not found")
    cur = db.connection.cursor()
    tmp = "name" if table=="Author" else "title"
    if plan == 1:
        cur.execute("SET SHOWPLAN_ALL ON")
    else:
        cur.execute("SET SHOWPLAN_ALL OFF")
    try:
        cur.execute(f"SELECT TOP {size} * FROM {table} WHERE {tmp} LIKE '{name}%';")
    except:
        raise HTTPException(status_code=501, detail="The database isn't connected")
    data = cur.fetchall()
    data = {
        "_source": data
    }
    return data



@app.get("/query/published_year")
async def query_published_year(size: int, year: int, plan:int):
    if db is None:
        return HTTPException(status_code=404, detail="Not found")
    cur = db.connection.cursor()
    if plan == 1:
        cur.execute("SET SHOWPLAN_ALL ON")
    else:
        cur.execute("SET SHOWPLAN_ALL OFF")
    try:
        cur.execute(f"SELECT TOP {size} * FROM Book WHERE published_year={year};")
    except:
        raise HTTPException(status_code=501, detail="The database isn't connected")
    data = cur.fetchall()
    data = {
        "_source": data
    }
    return data

@app.get("/query/genre")
async def query_books_belong_to_genre(size: int, genre: str, plan:int):
    if db is None:
        return HTTPException(status_code=404, detail="Not found")
    cur = db.connection.cursor()
    if plan == 1:
        cur.execute("SET SHOWPLAN_ALL ON")
    else:
        cur.execute("SET SHOWPLAN_ALL OFF")
    try:
        cur.execute(f"SELECT TOP {size} title FROM Book b JOIN Book_Genre bg ON b.id=bg.book_id WHERE bg.genre_id =(SELECT id from Genre WHERE name='{genre}');")
    except:
        raise HTTPException(status_code=501, detail="The database isn't connected")
    data = cur.fetchall()
    data = {
        "_source": data
    }
    return data



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)








        