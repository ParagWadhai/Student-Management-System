from fastapi import APIRouter, HTTPException, Path, Query
from models import StudentCreateRequest, StudentResponse, StudentUpdateRequest
from database import db
from bson import ObjectId
from typing import Optional, List

router = APIRouter()

def convert_mongo_id(student):
    student["id"] = str(student.pop("_id"))
    return student

# Create Student
@router.post("/students", response_model=dict, status_code=201)
async def create_student(student: StudentCreateRequest):
    student_data = student.dict()
    student_data["_id"] = str(ObjectId())
    await db.students.insert_one(student_data)
    return {"id": student_data["_id"]}

# List Students
@router.get("/students", response_model=dict)
async def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by minimum age")
):
    filters = {}
    if country:
        filters["address.country"] = country
    if age:
        filters["age"] = {"$gte": age}
    
    students = await db.students.find(filters).to_list(100)
    for student in students:
        student["id"] = student.pop("_id")
    return {"data": students}

# Fetch Student by ID
@router.get("/students/{id}", response_model=StudentResponse)
async def get_student(id: str = Path(..., description="Student ID")):
    student = await db.students.find_one({"_id": id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student["id"] = student.pop("_id")
    return student

# Update Student
@router.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: StudentUpdateRequest):
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    result = await db.students.update_one({"_id": id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

# Delete Student
@router.delete("/students/{id}", response_model=dict)
async def delete_student(id: str):
    result = await db.students.delete_one({"_id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
