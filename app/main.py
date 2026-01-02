from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, leads, customers, contacts, opportunities, admin
from app.database import engine, Base
from app.config import settings
from app.timezone import now

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM Application API",
    description="""
    FastAPI CRM with JWT Authentication
    
    ## Authentication
    1. Create a user via `/admin/init-admin` or `/users/`
    2. Login via `/auth/login` to get access_token
    3. Click the **Authorize** button (🔓) at the top right
    4. Enter your token in this format: `Bearer <your_access_token>`
    5. Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
    6. Click **Authorize** and then **Close**
    7. Now all protected endpoints will work
    
    ## Token Expiry
    - Access Token: 24 hours
    - Refresh Token: 60 days
    """,
    version="1.0.0"
)

# CORS middleware - allows frontend apps to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(leads.router)
app.include_router(customers.router)
app.include_router(contacts.router)
app.include_router(opportunities.router)

@app.get("/")
def root():
    return {"message": "CRM API is running"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timezone": settings.TIMEZONE,
        "server_time": now().isoformat()
    }
