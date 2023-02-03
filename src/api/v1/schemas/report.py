import uuid

data_schema = {
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "status": True,
                    "message": "The data has been added",
                }
            }
        },
    },
}

report_schema = {
    202: {
        "description": "Accepted",
        "content": {
            "application/json": {
                "example": {
                    "id": uuid.uuid4(),
                }
            }
        },
    },
}

