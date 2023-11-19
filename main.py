from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from src.routes import contacts, auth

app = FastAPI()

# Додавання обмеження швидкості для маршрутів контактів
app.add_middleware(
    FastAPILimiter(
        limits=[
            RateLimiter(times=10, seconds=3600, path="/api/contacts/", key_fn=lambda request: request.client_addr)
        ]
    )
)

# Додаємо роутери
app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}




