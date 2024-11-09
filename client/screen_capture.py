import mss
from PIL import Image
import io
import threading
import time

class ScreenCaptureManager:
    def __init__(self, compression_quality=50, scale_factor=0.75):
        self.compression_quality = compression_quality
        self.scale_factor = scale_factor
        self.last_frame = None
        self.lock = threading.Lock()
        self.thread_local = threading.local()
        self._running = True

    def get_mss(self):
        if not hasattr(self.thread_local, 'sct'):
            self.thread_local.sct = mss.mss()
        return self.thread_local.sct

    def capture_screen(self):
        try:
            sct = self.get_mss()
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            
            img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            
            new_size = (int(img.size[0] * self.scale_factor), 
                       int(img.size[1] * self.scale_factor))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=self.compression_quality)
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None

    def update_frame_loop(self):
        while self._running:
            try:
                new_frame = self.capture_screen()
                if new_frame is not None:
                    with self.lock:
                        self.last_frame = new_frame
                time.sleep(1/30)  # 30 FPS
            except Exception as e:
                print(f"Error in update loop: {e}")
                time.sleep(1)

    def get_current_frame(self):
        with self.lock:
            if self.last_frame is None:
                self.last_frame = self.capture_screen()
            if self.last_frame is None:
                return self._create_blank_frame()
            return io.BytesIO(self.last_frame.getvalue())

    def _create_blank_frame(self, width=800, height=600):
        img = Image.new('RGB', (width, height), color='black')
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer

    def start(self):
        self._running = True
        self.capture_thread = threading.Thread(target=self.update_frame_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()

    def stop(self):
        self._running = False
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join(timeout=1.0)