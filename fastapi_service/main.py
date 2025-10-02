from fastapi import FastAPI
app = FastAPI() 

@app.get("/tasks")
def get_tasks() :
    return {"tasks" : [] }