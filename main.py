from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import router
from DbHandler import init_db

init_db()
print("Initialized DB")


app = FastAPI()
# Allow requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

'''
@ToDo : Refine metadata
Refine
'''