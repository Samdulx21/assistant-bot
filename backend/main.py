from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import bot_route, test_route

app = FastAPI()

# origins = [
#     #"http://localhost.tiangolo.com",
#     #"https://localhost.tiangolo.com",
#     #"http://localhost"
#     "http://localhost:5173"
#     #"http://localhost:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ADD ROUTES

app.include_router(bot_route.router)
# app.include_router(test_route.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80000)

