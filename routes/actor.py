from flask import Blueprint
from controllers.actor import (
    create_actor,
    update_actor,
    delete_actor,
    search_actors,
    get_latest_actors,
    get_single_actor
)

actorRoutes = Blueprint('actorRoutes', __name__)

actorRoutes.add_url_rule(
    "/api/actor/create", view_func=create_actor, methods=["POST"])

actorRoutes.add_url_rule("/api/actor/update/<actorId>",
                         view_func=update_actor, methods=["POST"])
actorRoutes.add_url_rule("/api/actor/<actorId>",
                         view_func=delete_actor, methods=["DELETE"])
actorRoutes.add_url_rule(
    "/api/actor/search", view_func=search_actors, methods=["GET"])
actorRoutes.add_url_rule("/api/actor/latest-uploads",
                         view_func=get_latest_actors, methods=["GET"])
actorRoutes.add_url_rule("/api/actor/single/<actorId>",
                         view_func=get_single_actor, methods=["GET"])
