DIFFICULTY_SETTINGS = {
    "easy": {
        "time_limit": 30,
        "points": 10,
        "unlock_threshold": 50
    },
    "medium": {
        "time_limit": 20,
        "points": 15,
        "unlock_threshold": 75
    },
    "hard": {
        "time_limit": 15,
        "points": 20,
        "unlock_threshold": 100
    }
}

def get_difficulty_settings(level: str) -> dict:
    """Retourne les paramètres de difficulté"""
    return DIFFICULTY_SETTINGS.get(level.lower(), DIFFICULTY_SETTINGS["easy"])