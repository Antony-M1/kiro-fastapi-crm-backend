from fastapi import FastAPI
from app.routers import auth, users, leads, customers, contacts, opportunities, admin
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM Application API",
    description="FastAPI CRM with JWT Authentication",
    version="1.0.0"
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
    return {"status": "healthy"}
