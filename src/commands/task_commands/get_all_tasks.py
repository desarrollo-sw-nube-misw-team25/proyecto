from flask import Flask, jsonify, request
from src.extensions import celery
from src.models.video_model import Video
from functools import wraps
import os


def get_all_tasks(max_results=None, order=0):
    try:
        inspector = celery.control.inspect()

        query = Video.query
        if order == 1:
            query = query.order_by(Video.id.desc())
        else:
            query = query.order_by(Video.id.asc())

        if max_results is not None:
            query = query.limit(max_results)

        videos = query.all()
        tasks_info = [{'id': video.id, 'state': video.status, 'filename': video.filename, 'timestamp': video.timestamp} for video in videos]

        return jsonify(tasks_info)
    except Exception as e:
        response = jsonify({'error': str(e)})
        response.status_code = 500
        return response
