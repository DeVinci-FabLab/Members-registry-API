# app/main.py
import sys
sys.path.append("/app")

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import member as member_router
from app.api.routes import promotion as promotion_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Application started and database tables created!")
    yield
    print("🛑 Application shutting down!")

# ✅ Crée une seule fois l'application
app = FastAPI(lifespan=lifespan)

# ✅ Déclare les routes après
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ✅ Ajoute le routeur
app.include_router(member_router.router)
app.include_router(promotion_router.router)

# ✅ Entrée locale
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
