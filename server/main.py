from fastapi import FastAPI, WebSocket, HTTPException, Response
from fastapi.responses import StreamingResponse
import json
import base64
import io
from typing import Dict
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

# In-memory storage for latest frames
frames: Dict[str, bytes] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            client_id = message['client_id']
            # Convert base64 frame to bytes and store it
            frame_bytes = base64.b64decode(message['frame'])
            frames[client_id] = frame_bytes
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/screen/{client_id}.jpg")
async def get_screen(client_id: str):
    if client_id not in frames:
        # Create a blank frame if no frame is available
        from PIL import Image
        img = Image.new('RGB', (800, 600), color='black')
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/jpeg")
    
    # Return the latest frame
    return Response(content=frames[client_id], media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)