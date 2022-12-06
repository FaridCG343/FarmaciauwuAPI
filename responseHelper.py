def set_custom_response(description: str, example: dict or list):
    return {
        "description": description,
        "content": {
            "application/json": {
                "schema": {
                    "example": example
                }
            }
        }
    }


def set_401_response():
    return {
        "description": "Unauthorized",
        "content": {
            "application/json": {
                "schema": {
                    "example": {"details": {"message": "You cannot perform this action due to lack of permissions."}}
                }
            }
        }
    }


def set_404_response():
    return {
        "description": "Not found",
        "content": {
            "application/json": {
                "schema": {
                    "example": {"details": {"message": "Not found"}}
                }
            }
        }
    }


def set_409_response():
    return {
        "description": "Conflict",
        "content": {
            "application/json": {
                "schema": {
                    "example": {"details": {"message": "There's already an existing record"}}
                }
            }
        }
    }