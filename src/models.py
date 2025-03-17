from pydantic import BaseModel

class Information(BaseModel):
    name: str
    nick_name: str
    group: str
    
class TelegramUpdate(BaseModel):
    message: dict