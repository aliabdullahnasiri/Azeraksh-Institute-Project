import json
import math
import os
from datetime import datetime as dt
from typing import Dict, List

from flask import Response, current_app, request, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from .. import bp


@bp.post("/upload")
@login_required
def upload() -> Response:
    response: Response = Response(headers={"Content-Type": "application/app"})

    lst: List[Dict] = []

    for file in request.files.values():
        dst = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            today := dt.now().strftime("%Y-%m-%d"),
        )

        os.makedirs(dst, exist_ok=True)

        if file.filename:
            file.save(
                os.path.join(
                    dst,
                    filename := f"{math.floor(dt.now().timestamp())}_{secure_filename(file.filename)}",
                )
            )

            lst.append(
                {
                    "message": "File successfully uploaded.",
                    "file": {
                        "name": file.filename,
                        "url": url_for(
                            "static", filename=f"uploads/{today}/{filename}"
                        ),
                    },
                    "status": 200,
                }
            )

    response.response = json.dumps(lst)

    return response
