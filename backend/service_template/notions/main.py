from fastapi import FastAPI, Query, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, date
import os
class Recipient(BaseModel):
    to: str
    name: str
    amount: float
    date: str
    template: str


class TodayResponse(BaseModel):
    phone_number: str
    language: str
    recipients: list[Recipient]


def calculateDays(date: str) -> int:
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    return (date_obj - datetime.now()).days


def pickTemplate(days: int) -> str:
    if days <= 0: 
        return "moroso"
    if days == 0: 
        return "moroso"
    if days <= 5: 
        return "moroso"
    if days <= 10: 
        return "moroso"
    if days <= 15: 
        return "moroso"
    return "template_default"


def create_app() -> FastAPI:
    application = FastAPI(
        title="Notions API", 
        version="1.0.0",
        default_response_class=JSONResponse
    )
    WA_PHONE_NUMBER = os.getenv("WA_PHONE_NUMBER","default")
    WA_LANG=os.getenv("WA_LANG","Spanish (MEX)")
    # Zona horaria - usando UTC por simplicidad
    Zona = "UTC"
    Clients=[
        {"to":"+573012706204","name":"Milo", "amount": "200.000","date":"2025-09-05"},
        {"to":"+573174929988","name":"Santi idarraga", "amount": "200.000","date":"2025-09-20"}
    ]
    
    @application.get("/")
    def root():
        return {"message": "Notions API is running!"}
    
    @application.get("/notions/today/json", response_class=JSONResponse)
    def get_notions_today_json(
        includeAll: bool = Query(False, description="Include all clients"),
        specialDays: str = Query("15,10,5,0,neg", description="Special days to include, neg<0")
    ):
        """Endpoint específico para Make que garantiza Content-Type: application/json"""
        # Interpretar filtro de días de forma más legible
        allowed_days = set()
        day_tokens = specialDays.split(",")
        
        for token in day_tokens:
            clean_token = token.strip()
            
            if not clean_token:
                continue
            if clean_token.lower() == "neg":
                allowed_days.add("neg")
            else:
                try:
                    day_number = int(clean_token)
                    allowed_days.add(day_number)
                except ValueError:
                    pass
        
        recipients: list[Recipient] = []
        
        for client in Clients:
            days = calculateDays(client["date"])
            template = pickTemplate(days)
            recipients.append(Recipient(
                to=client["to"], 
                name=client["name"], 
                amount=float(client["amount"]), 
                date=client["date"], 
                template=template
            ))
        
        response_data = TodayResponse(
            phone_number=WA_PHONE_NUMBER, 
            language=WA_LANG, 
            recipients=recipients
        )
        return JSONResponse(
            content=response_data.model_dump(),
            headers={"Content-Type": "application/json"}
        )
    
    @application.get("/notions/today", response_model=TodayResponse)
    def get_notions_today(
        includeAll: bool = Query(False, description="Include all clients"),
        specialDays: str = Query("15,10,5,0,neg", description="Special days to include, neg<0")
    ) -> TodayResponse:
        # Interpretar filtro de días de forma más legible
        allowed_days = set()
        day_tokens = specialDays.split(",")
        
        for token in day_tokens:
            clean_token = token.strip()
            
            if not clean_token:
                continue
            if clean_token.lower() == "neg":
                allowed_days.add("neg")
            else:
                try:
                    day_number = int(clean_token)
                    allowed_days.add(day_number)
                except ValueError:
                    pass
        recipients: list[Recipient] = []
        
        for client in Clients:
            days = calculateDays(client["date"])
            template = pickTemplate(days)
            recipients.append(Recipient(
                to=client["to"], 
                name=client["name"], 
                amount=float(client["amount"]), 
                date=client["date"], 
                template=template
            ))
        
        return TodayResponse(
            phone_number=WA_PHONE_NUMBER, 
            language=WA_LANG, 
            recipients=recipients
        )

    return application


app = create_app()

