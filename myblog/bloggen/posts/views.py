from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from bloggen import db
from bloggen.models import Blogpost
# from bloggen.posts.forms import BlogPostForm


blog_posts = Blueprint('blog_posts', __name__)

@blog_posts.route('/posts', methods=['GET', 'POST'])
def posts():
    all_posts = Blogpost.query.all()
    return render_template('posts.html', all_posts=all_posts)
    

@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    # form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = Blogpost(title=form.title.data,
                            text=form.text.data,
                            user_id=current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog post has created!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    return render_template('single_post.html', post=blog_post)


@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        # blog_post.categories.allappend(form.category.data)

        db.session.commit()
        flash('Blog post has Updated!')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.category.data = blog_post.categories
        form.text.data = blog_post.text

    return render_template('create_post.html', form=form)


@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(blog_post_id):
    blog_post = Blogpost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post has been deleted!')
    
    return redirect(url_for('core.index'))