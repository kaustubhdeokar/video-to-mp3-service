import pika, json, tempfile, os
import threading
import subprocess
from bson.objectid import ObjectId
import moviepy.editor as mp

def callback(ch, method, properties, body):
    try:
        print(f" [x] Received {body}")
        message = json.loads(body)
        video_fid = message["video_fid"]
        username = message["username"]
        
        mongo_video_client = MongoClient("mongodb://localhost:27017/")
        mongo_video_db = mongo_video_client["videos"]
        fs_videos = gridfs.GridFS(mongo_video_db)
        video = fs_videos.get(ObjectId(video_fid))

        video_path = f"/tmp/{video_fid}.mp4"
        with open(video_path, "wb") as f:
            f.write(video.read())
        
        audio_path = f"/tmp/{video_fid}.mp3"
        video_clip = mp.VideoFileClip(video_path)
        video_clip.audio.write_audiofile(audio_path)

        with open(audio_path, "rb") as f:
            audio_fid = fs_videos.put(f, filename=f"{video_fid}.mp3")

        print(f"Video {video_fid} converted to audio {audio_fid} for user {username}")
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        # Optionally, you can reject the message and requeue it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def consume_messages():
    print('Connect to RabbitMQ and consuming messages')
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue='video', durable=True)
    # Set up subscription on the queue
    channel.basic_consume(
        queue='video',
        on_message_callback=callback,
        auto_ack=True
    )
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def start_consumer_thread():
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

if __name__ == "__main__":
    consume_messages()