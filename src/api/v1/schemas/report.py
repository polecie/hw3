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
            "application/json": {"example": {"status": True, "message": f"The report {uuid.uuid4()} is processing"}}
        },
    },
}

get_report_schema = {
    404: {
        "description": "Not Found",
        "content": {"application/json": {"example": {"detail": "report not found"}}},
    },
    200: {
        "description": "No Content",
        "content": {
            "application/json": {
                "examples": {
                    "received": {"summary": "Отчет получен", "value": {"detail": "the report was received"}},
                    "processing": {
                        "summary": "Отчет в обработке",
                        "value": {"detail": "the report is not yet ready, state is PENDING"},
                    },
                }
            }
        },
    },
}
