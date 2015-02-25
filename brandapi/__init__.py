from flask import Flask, render_template, abort, make_response, jsonify
from werkzeug.contrib.fixers import ProxyFix


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # Register blueprints
    #from brandapi.scores_v1.views import scores
    #app.register_blueprint(scores, url_prefix='/brands/api/v1/scores')
    return app


# Boostrap Flask App
app = create_app('brandapi.config')
app_config = app.config


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run()
