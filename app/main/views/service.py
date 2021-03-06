from datetime import datetime
from uuid import uuid4
from flask import jsonify, abort, current_app
from .. import main
from app import db
from app.main.views import get_json_from_request
from app.models import Service, Token, User, Usage
from app.main.validators import valid_service_submission
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc
from app.main.auth.token_auth import token_type_required


def user_is_a_platform_admin(user_id):
    user = User.query.get(user_id)
    if user is not None and user.role == 'platform-admin':
        return True
    return False


@main.route('/service/<int:service_id>/users', methods=['GET'])
@token_type_required('admin')
def fetch_users_for_service(service_id):
    service = Service.query.get(service_id)

    if service:
        return jsonify(
            users=[user.serialize() for user in service.users]
        )
    else:
        abort(404, "service not found")


@main.route('/user/<int:user_id>/service/<int:service_id>', methods=['GET'])
@token_type_required('admin')
def fetch_service_by_user_id_and_service_id(user_id, service_id):
    if user_is_a_platform_admin(user_id):
        service = Service.query.get(service_id)
    else:
        service = Service.query.filter(
            Service.id == service_id,
            Service.users.any(id=user_id)
        ).first_or_404()

    return jsonify(
        service=service.serialize()
    )


@main.route('/service/<int:service_id>/usage', methods=['GET'])
@token_type_required('admin')
def fetch_usage_for_service(service_id):
    all_the_usage = Usage.query.filter(Usage.service_id == service_id).order_by(desc(Usage.day)).all()

    return jsonify(
        usage=[usage.serialize() for usage in all_the_usage]
    )


@main.route('/user/<int:user_id>/services', methods=['GET'])
@token_type_required('admin')
def fetch_services_by_user(user_id):
    if user_is_a_platform_admin(user_id):
        services = Service.query.order_by(desc(Service.created_at)).all()
    else:
        services = Service.query.filter(
            Service.users.any(id=user_id)
        ).order_by(desc(Service.created_at)).all()

    return jsonify(
        services=[service.serialize() for service in services]
    )


@main.route('/service/<int:service_id>/activate', methods=['POST'])
@token_type_required('admin')
def activate_service(service_id):
    service = Service.query.get(service_id)

    if not service:
        abort(404, "Service not found")

    service.active = True
    try:
        db.session.add(service)
        db.session.commit()
        return jsonify(service=service.serialize())
    except IntegrityError as e:
        print(e.orig)
        db.session.rollback()
        abort(400, "failed to activate service")


@main.route('/service/<int:service_id>/deactivate', methods=['POST'])
@token_type_required('admin')
def deactivate_service(service_id):
    service = Service.query.get(service_id)

    if not service:
        abort(404, "Service not found")

    service.active = False
    try:
        db.session.add(service)
        db.session.commit()
        return jsonify(service=service.serialize())
    except IntegrityError as e:
        print(e.orig)
        db.session.rollback()
        abort(400, "failed to activate service")


@main.route('/service', methods=['POST'])
@token_type_required('admin')
def create_service():
    service_from_request = get_json_from_request('service')

    validation_result, validation_errors = valid_service_submission(service_from_request)
    if not validation_result:
        return jsonify(
            error="Invalid JSON",
            error_details=validation_errors
        ), 400

    user = User.query.get(service_from_request['userId'])

    if not user:
        return jsonify(
            error="failed to create service - invalid user"
        ), 400

    try:
        token = Token(token=uuid4(), type='client')
        db.session.add(token)
        db.session.flush()

        service = Service(
            name=service_from_request['name'],
            created_at=datetime.utcnow(),
            token_id=token.id,
            active=True,
            restricted=True,
            limit=current_app.config['MAX_SERVICE_LIMIT']
        )
        service.users.append(user)
        db.session.add(service)
        db.session.commit()
        return jsonify(
            service=service.serialize()
        ), 201
    except IntegrityError as e:
        print(e.orig)
        db.session.rollback()
        abort(400, "failed to create service")


@main.route('/service/<int:service_id>/unrestrict', methods=['POST'])
@token_type_required('admin')
def unrestrict_service(service_id):
    service = Service.query.get(service_id)

    if not service:
        abort(404, "Service not found")

    service.restricted = False
    try:
        db.session.add(service)
        db.session.commit()
        return jsonify(service=service.serialize())
    except IntegrityError as e:
        print(e.orig)
        db.session.rollback()
        abort(400, "failed to activate service")


@main.route('/service/<int:service_id>/restrict', methods=['POST'])
@token_type_required('admin')
def restrict_service(service_id):
    service = Service.query.get(service_id)

    if not service:
        abort(404, "Service not found")

    service.restricted = True
    try:
        db.session.add(service)
        db.session.commit()
        return jsonify(service=service.serialize())
    except IntegrityError as e:
        print(e.orig)
        db.session.rollback()
        abort(400, "failed to activate service")
