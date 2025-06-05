from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
import route_user
from chat.router import router as chat_router  # ✅ Import chat router

# ✅ Initialize app
app = FastAPI()

# ✅ CORS middleware (connects to React at localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create database tables
Base.metadata.create_all(bind=engine)

# ✅ Register user routes (login/signup)
app.include_router(route_user.router)

# ✅ Register chat routes with /chat prefix
app.include_router(chat_router, prefix="/chat")

