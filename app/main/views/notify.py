from flask import jsonify, url_for, current_app

from .. import main


@main.route('/')
def index():
    """Entry point for the API, show the resources that are available."""
    return jsonify(links={
        "notification.create": {
            "url": url_for(
                '.create_notification',
                _external=True,
                _scheme=current_app.config.get('NOTIFY_HTTP_PROTO', 'http')
            ),
            "method": "POST"
        }
    }
    ), 200


@main.route('/notification', methods=['POST'])
def create_notification():
    return jsonify(
        message="I made a notification"
    )
