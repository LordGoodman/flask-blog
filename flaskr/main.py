import os

from flask import Flask
import db, auth, blog
# import db, auth

def createFlaskApp(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path) 
    except OSError:
        pass
    
    db.initDB(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app

if __name__ == "__main__":
    app = createFlaskApp()
    app.run(port=8888)