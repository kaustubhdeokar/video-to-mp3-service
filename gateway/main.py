import os, gridfs, pika, json 
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from pymongo import MongoClient
from bson.objectid import ObjectId

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
from consumer import start_consumer_thread
import httpx

from mongoutil import fs_videos, fs_mp3s

app = FastAPI()

# Dependency to validate requests
def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = validate(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='video', durable=True)

@app.on_event("startup")
async def startup_event():
    start_consumer_thread()

# # MongoDB connections
# video_client = MongoClient("mongodb://172.17.0.2:27017/")
# #mongo_video_client = MongoClient("mongodb://localhost:27017/")
# video_db = video_client["videos"]
# fs_videos = gridfs.GridFS(video_db)

# mp3_client = MongoClient("mongodb://172.17.0.2:27017/")
# mp3_db = mp3_client["mp3s"]
# fs_mp3s = gridfs.GridFS(mp3_db)

async def validate_user(token: str):
    async with httpx.AsyncClient() as client:
        token = token.split(" ")[1]
        print(token)
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(f"http://localhost:8000/validate", headers=headers)
        if response.status_code == 200:
            return response
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(request: Request):
    token = request.headers.get("Authorization")
    print(token)
    response = await validate_user(token)
    print(response.json())
    return 'user'

@app.get("/")
def base_call():
    return {"msg":"running."}

@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    try:
        video_id = fs_videos.put(file.file, filename=file.filename)
        message = {
            "video_fid": str(video_id),
            "mp3_fid": None,
            "username": 'user2',
        }
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while uploading video: {e}")
        fs_videos.delete(video_id)
    return {"video_id": str(video_id)}


@app.get("/download_video/{video_id}")
async def download_video(video_id: str):
    video = fs_videos.get(ObjectId(video_id))
    return StreamingResponse(video, media_type="video/mp4", headers={"Content-Disposition": f"attachment; filename={video.filename}"})