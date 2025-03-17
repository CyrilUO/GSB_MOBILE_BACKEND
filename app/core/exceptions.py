from enum import Enum

from fastapi import HTTPException, status


# Liste d'errors enum

class ErrorEnum(str, Enum):
    UNAUTHORIZED = "You are not authorized to perform this action."
    NOT_FOUND = "The requested resource was not found."
    INVALID_CREDENTIALS = "Invalid email or password."
    DUPLICATE_ENTRY = "This entry already exists."
    VALIDATION_ERROR = "Invalid input data."


class HarmFullEnum(str, Enum):
    # Common profanities
    FUCK = "Fuck"
    SHIT = "Shit"
    BITCH = "Bitch"
    ASSHOLE = "Asshole"
    BASTARD = "Bastard"
    DICK = "Dick"
    CUNT = "Cunt"

    # Racial slurs (obfuscated here for clarity)
    N_WORD = "N-word"
    K_WORD = "K-word"
    C_WORD = "C-word"

    # Hate speech and violent expressions
    KILL = "Kill"
    MURDER = "Murder"
    RAPE = "Rape"
    GENOCIDE = "Genocide"
    BOMB = "Bomb"
    TERRORIST = "Terrorist"
    PEDO = "Pedo"
    NAZI = "Nazi"

    # Self-harm & suicide-related words
    SUICIDE = "Suicide"
    CUTTING = "Cutting"
    DIE = "Die"
    JUMP = "Jump"

    @classmethod
    def banned_words(cls):
        return {word.value.lower() for word in cls.__members__.values()}
