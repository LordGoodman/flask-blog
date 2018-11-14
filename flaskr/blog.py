from flask import Blueprint, flash, g, redirect, render_template, url_for, request
from auth import login_required
from db import createBlog
from werkzeug.exceptions import abort
from model import user as userModel, blog as blogModel, blogSchema

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    posts = []
    userSet = userModel.objects()

    for user in userSet:
        blogSet = blogModel.objects(authorId=user.id)
        # dump will return mashllom when only one receive value was provided
        blogsForAUser = blogSchema(many=True).dump(blogSet).data
        for b in blogsForAUser:
            b["username"] = user.username

        posts.extend(blogsForAUser)

    posts.sort(key=lambda x: x['created'], reverse=True)
    return render_template('blog/index.html', posts=posts) 

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
    
        if title is None:
            error = 'title is empty'
        elif body is None:
            error = 'body is empty'
    
        if error is not None:
            flash(error)
        else:
            createBlog(title=title, body=body, authorId=g.user.id)
            return redirect(url_for('index'))
    
    return render_template('blog/create.html')

@bp.route('/<string:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = getPost(id)
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if title is None:
            error = "title is empty"
        
        if error is not None:
            flash(error)
        else:
            blogModel.objects(id=post['id']).update_one(title=title,
                                                        body=body)
            return redirect(url_for('index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<string:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = getPost(id)
    blogModel.objects(id=id).delete()
    return redirect(url_for('index'))

def getPost(id, check_author=True):
    try:
        post = blogModel.objects.get(id=id) 
    except Execption as e:
        abort(404, "Post: {} not found".format(id))
    
    if check_author and post.authorId != g.user.id:
        abort(403)
    
    return blogSchema().dump(post).data
