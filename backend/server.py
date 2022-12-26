from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path

# For debugging purposes, allows us to create playground for testing queries 
from ariadne.constants import PLAYGROUND_HTML 

from models.course import courseQuery
from utils.utils import log, LoggingMode, DEBUG_LOG_ON

app = Flask(__name__)

# Load schema from file, and validate with `gql` 
type_defs = gql(load_schema_from_path("schemas/course.graphql"))
schema = make_executable_schema(type_defs, courseQuery)

@app.route('/')
def index():
    return 'Hello World'

# Playground (Can remove for produciton) 
@app.route('/graphql', methods=['GET'])
def graphql_playground():
    """Serve GraphiQL playground"""
    return PLAYGROUND_HTML, 200

# GraphQL endpoint
@app.route('/graphql', methods=['POST'])
def graphql_server():
    """GraphQL Request Endpoint"""

    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400

    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=DEBUG_LOG_ON)