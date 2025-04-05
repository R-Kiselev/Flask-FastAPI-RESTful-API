from fastapi import APIRouter, Depends, status, HTTPException, Request
from bson import ObjectId

from ..schemas.logs import LogSchema
from ..db import get_db_client
from ..config import settings
from motor.motor_asyncio import AsyncIOMotorCursor
from ..pagination import paginate


# Use the APIRouter class to create a new router. 
# This router will be used to define the routes for the logs resource.
# Then this router will be included in the main FastAPI app.
router = APIRouter()
mongodb_collection = settings.get_mongodb_collection('logs')


@router.get("/logs")
async def get_logs(request: Request, db=Depends(get_db_client)):
    logs = db[mongodb_collection].find()
    return await paginate(request, logs, LogSchema)


@router.post("/logs", response_model=LogSchema, status_code=status.HTTP_201_CREATED)
async def create_log(log: LogSchema, db=Depends(get_db_client)):
    # Returns mongodb document object, not a dict
    inserted_doc = await db[mongodb_collection].insert_one(log.model_dump())

    # Get the inserted document from the database, dict format
    created_log = await db[mongodb_collection].find_one({"_id": inserted_doc.inserted_id})
    return created_log


@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(log_id: str, db=Depends(get_db_client)):
    try:
        ObjectId(log_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid log ID")

    result = await db[mongodb_collection].delete_one({"_id": ObjectId(log_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log not found")
