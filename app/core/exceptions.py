from enum import Enum

from fastapi import HTTPException, status

class ErrorEnum(str, Enum):
    UNAUTHORIZED = "You are not authorized to perform this action."
    NOT_FOUND = "The requested resource was not found."
    INVALID_CREDENTIALS = "Invalid email or password."
    DUPLICATE_ENTRY = "This entry already exists."
    VALIDATION_ERROR = "Invalid input data."


