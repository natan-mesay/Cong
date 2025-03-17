from pydantic import BaseModel

class Information(BaseModel):
    name: str
    nick_name: str
    group: str
    
class TelegramMessage(BaseModel):
    chat_id: int
    text: str