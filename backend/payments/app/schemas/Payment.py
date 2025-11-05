from typing import Optional

from pydantic import BaseModel, Field


class PaymentInitializationRequest(BaseModel):
    """Request schema for initializing a payment."""
    
    client_id: int = Field(..., description="ID of the client")
    credit_id: Optional[int] = Field(None, description="Optional specific credit ID. If not provided, all credits will be sent.")


class PaymentInitializationResponse(BaseModel):
    """Response schema from payment gateway."""
    
    success: bool
    sessionId: str
    paymentUrl: str
    expiresIn: int
    message: str


class PaymentErrorResponse(BaseModel):
    """Error response schema."""
    
    success: bool = False
    error: str

