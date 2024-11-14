import mss
from PIL import Image
import io
import asyncio
import websockets
import json
import base64
import os
from dotenv import load_dotenv

class ScreenCaptureClient:
    def __init__(self, compression_quality=50, scale_factor=0.75):
        self.compression_quality = compression_quality
        self.scale_factor = scale_factor
        self.sct = mss.mss()
        self._running = True
        load_dotenv()
        self.server_url = os.getenv('SERVER_URL', 'ws://localhost:8000/ws')
        self.client_id = os.getenv('CLIENT_ID', 'default-client')

    async def capture_and_send(self, websocket):
        while self._running:
            try:
                # Capture screen
                monitor = self.sct.monitors[1]  # Primary monitor
                screenshot = self.sct.grab(monitor)
                
                img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                new_size = (int(img.size[0] * self.scale_factor), 
                           int(img.size[1] * self.scale_factor))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=self.compression_quality)
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                # Send frame
                message = {
                    'client_id': self.client_id,
                    'frame': base64_image
                }
                await websocket.send(json.dumps(message))
                await asyncio.sleep(1/30)  # 30 FPS
                
            except Exception as e:
                print(f"Error in capture loop: {e}")
                await asyncio.sleep(1)

    async def connect(self):
        while True:
            try:
                async with websockets.connect(self.server_url) as websocket:
                    print(f"Connected to server at {self.server_url}")
                    await self.capture_and_send(websocket)
                    websocket.close()
            except Exception as e:
                print(f"Connection error: {e}")
                await asyncio.sleep(5)  # Wait before reconnecting

    def start(self):
        asyncio.run(self.connect())

    def stop(self):
        self._running = False

# client/main.py
if __name__ == "__main__":
    client = ScreenCaptureClient(compression_quality=60, scale_factor=0.75)
    try:
        client.start()
    except KeyboardInterrupt:
        client.stop()