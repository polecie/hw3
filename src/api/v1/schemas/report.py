import uuid

put_data_schema = {
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
    400: {
        "description": "Bad Request",
        "content": {"application/json": {"example": {"detail": "data has not been added"}}},
    },
}

create_report_schema = {
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

get_report_schema = {
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "report not found"}}},
    },
    202: {
        "description": "Accepted",
        "content": {"application/json": {"example": {"detail": "the report is not yet ready"}}},
    },
    200: {
        "description": "Successful Response",
        "content": {"application/json": {"example": {"detail": "the report was received"}}},
    },
}
