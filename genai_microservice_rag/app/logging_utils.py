import json, sys, time, logging

class JsonLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        self.addHandler(handler)
        self.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": int(time.time()),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)

logger = JsonLogger("app")
