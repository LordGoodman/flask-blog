from mongoengine import connect
from model import user, blog, userSchema, blogSchema
from uuid import uuid4
import click
from flask.cli import with_appcontext
from datetime import datetime as dt

def connectDB(app):
    connect(db=app.config.get("MONGODB_DB", "local"),
            host=app.config.get("MONGODB_HOST", "localhost"),
            port=app.config.get("MONGODB_PORT", 27017),
            username=app.config.get("MONGODB_USER", ""),
            password=app.config.get("MONGODB_PASS")
            )

def cleanDB():
    users = user.objects
    blogs = blog.objects

    for u in users:
        u.delete()
    
    for b in blogs:
        b.delete()

def initDB(app):
    connectDB(app)
    #cleanDB()
    #user.delete()
    #blog.delete()

def registerUser(username, password):
    uid = uuid4().hex
    u = user(id=uid, username=username, password=password)
    u.save()

def createBlog(authorId, title, body):
    bid = uuid4().hex
    b = blog(id=bid, authorId=authorId, title=title, body=body)
    b.save()

'''
@click.command('init-db')
@with_appcontext
def initDBCommand():
    initDB()
    click.echo("Initialized the database.")

def initApp(app):
    initDB(app)
    app.cli.add_command(initDBCommand)
'''