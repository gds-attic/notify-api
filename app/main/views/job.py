from flask import jsonify, abort
from .. import main
from app import db
from app.main.views import get_json_from_request
from app.models import Job, Service
from app.main.validators import valid_job_submission
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from app.main.auth.token_auth import token_type_required


@main.route('/job/<int:job_id>', methods=['GET'])
@token_type_required('admin')
def fetch_job(job_id):
    job = Job.query.filter(Job.id == job_id).first_or_404()

    return jsonify(
        job=job.serialize()
    )


@main.route('/service/<int:service_id>/jobs', methods=['GET'])
@token_type_required('admin')
def fetch_jobs_by_service(service_id):
    jobs = Job.query.join(Service).filter(
        Service.id == service_id
    ).order_by(desc(Job.created_at)).all()

    return jsonify(
        jobs=[job.serialize() for job in jobs]
    )


@main.route('/job', methods=['POST'])
@token_type_required('admin')
def create_job():
    job_from_request = get_json_from_request('job')

    validation_result, validation_errors = valid_job_submission(job_from_request)
    if not validation_result:
        return jsonify(
            error="Invalid JSON",
            error_details=validation_errors
        ), 400

    job = Job(
        name=job_from_request['name'],
        service_id=job_from_request['serviceId'],
        created_at=datetime.utcnow()
    )

    if "filename" in job_from_request:
        job.filename = job_from_request['filename']

    try:
        db.session.add(job)
        db.session.commit()
        return jsonify(
            job=job.serialize()
        ), 201
    except IntegrityError as e:
        db.session.rollback()
        abort(400, e.orig)
