from fastapi import FastAPI
from routes.student_routes import router as student_router

app = FastAPI(
    title="Backend Intern Hiring Task",
    description="APIs for Student Management System",
    version="1.0.0",
)

# Include student routes
app.include_router(student_router)

# Add a root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Management System API!"}
