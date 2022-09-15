from flask import Blueprint
from controllers.movie import (
    upload_trailer
)

movieRoutes = Blueprint('movieRoutes', __name__)

movieRoutes.add_url_rule("/api/movie/upload-trailer",
                         view_func=upload_trailer, methods=["POST"])
