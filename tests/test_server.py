try:
    from flask import Flask, request
    app = Flask(__name__)

    @app.route('/method',
               methods=['GET',
                        'POST',
                        'PUT',
                        'PATCH',
                        'DELETE'])
    def hello_world():
        return request.method

except ImportError:
    app = None
