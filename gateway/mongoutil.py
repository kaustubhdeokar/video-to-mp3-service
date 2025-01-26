
import os, gridfs, pika, json 
from pymongo import MongoClient

video_client = MongoClient("mongodb://172.17.0.2:27017/")
#mongo_video_client = MongoClient("mongodb://localhost:27017/")
video_db = video_client["videos"]
fs_videos = gridfs.GridFS(video_db)

mp3_client = MongoClient("mongodb://172.17.0.2:27017/")
mp3_db = mp3_client["mp3s"]
fs_mp3s = gridfs.GridFS(mp3_db)