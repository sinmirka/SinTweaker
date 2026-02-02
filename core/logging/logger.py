from datetime import datetime

class Logger:
    def __init__(self):
        self.started_at = datetime.now().strftime("%H:%M:%S")
        self.buffer = []
        
        self.buffer.append(f"[{self.started_at}] Initialized")
    
    def log(self, text: str | None):
        if not text:
            return
        time = datetime.now().strftime("%H:%M:%S")
        line = f"[{time}] {text}"
        self.buffer.append(line)
        self.flush()
    
    def flush(self) -> str:
        return "\n".join(self.buffer)