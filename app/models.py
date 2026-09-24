from pydantic import BaseModel, Field

class UserAuth(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "fashion_lover"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "securePass123"})

class CartItemRequest(BaseModel):
    cloth_id: int = Field(..., json_schema_extra={"example": 1})
    quantity: int = Field(..., ge=1, json_schema_extra={"example": 2})

class PaymentRequest(BaseModel):
    card_number: str = Field(..., min_length=16, max_length=16, json_schema_extra={"example": "1234567812345678"})
    expiry: str = Field(..., json_schema_extra={"example": "12/29"})
    cvv: str = Field(..., min_length=3, max_length=3, json_schema_extra={"example": "123"})
