from flask import Blueprint, jsonify
from services.calculator import calculate_summary

summary_bp = Blueprint('summary', __name__, url_prefix='/api/summary')

@summary_bp.route('/', methods=['GET'])
def get_summary():
    result = calculate_summary()
    return jsonify(result)
