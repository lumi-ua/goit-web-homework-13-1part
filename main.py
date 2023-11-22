from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.middleware.cors import CORSMiddleware

import redis.asyncio as redis

from src.routes import contacts, auth, users
from src.conf.config import settings


app = FastAPI()

origins = [ 
    "http://localhost:3000", "http://127.0.0.1:5500"
    ]


async def startup_event():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)

app.add_event_handler("startup", startup_event)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# Додаємо роутери
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}




