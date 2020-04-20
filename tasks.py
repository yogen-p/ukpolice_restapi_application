from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import current_user

# Defining blueprint
td_demo = Blueprint('td_demo', __name__)

from app import User, ToDo, db

# Display to-do page
@td_demo.route('/todo')
def todo():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('todo.html')
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Display taksks for logged-in user
@td_demo.route('/tasks')
def tasks():
    if current_user.is_authenticated:  # Get all tasks for logged-in user
        cursor = ToDo.query.filter_by(email=current_user.email).all()
        if cursor:
            tasks = [row.serialize() for row in cursor]  # Make sql row json compatible
            return jsonify({'code': '200',
                            'tasks': tasks}), 200
        else:
            return jsonify({'code': '404',
                            'error': 'Not Found'}), 404
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Filter tasks by status
@td_demo.route('/tasks/status=<stat>')
def task_status(stat):
    if current_user.is_authenticated:  # Get task with status for valid user
        cursor = ToDo.query.filter_by(email=current_user.email, status=stat).all()
        if cursor:
            tasks = [row.serialize() for row in cursor]  # Make sql row json compatible
            return jsonify({'code': '200',
                            'tasks': tasks}), 200
        else:
            return jsonify({'code': '404',
                            'error': 'Not Found'}), 404
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Filter tasks by title
@td_demo.route('/tasks/title=<ttl>')
def task_title(ttl):
    if current_user.is_authenticated:  # Get task with title for valid user
        cursor = ToDo.query.filter_by(email=current_user.email, title=ttl).all()
        if cursor:
            tasks = [row.serialize() for row in cursor]  # Make sql row json compatible
            return jsonify({'code': '200',
                            'tasks': tasks}), 200
        else:
            return jsonify({'code': '404',
                            'error': 'Not Found'}), 404
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Dislpay add task page
@td_demo.route('/atask')
def atask():
    if current_user.is_authenticated:
        return render_template('add_task.html')
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Performing add task
@td_demo.route('/atask', methods=['POST'])
def atask_post():
    if current_user.is_authenticated:
        title = request.form.get('title')  # Get input from form
        desc = request.form.get('desc')
        email = current_user.email
        new_task = ToDo(email=email, title=title, desc=desc, status='False')  # Create task
        db.session.add(new_task)  # Add task to database
        db.session.commit()
        return jsonify({'code': '201',
                        'response': 'Created'}), 201
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Display delete task page
@td_demo.route('/dtask')
def dtask():
    if current_user.is_authenticated:  # Check for valid user
        return render_template('del_task.html')
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Performing delete task
@td_demo.route('/dtask', methods=['POST', 'DELETE'])
def dtask_del():
    title = request.form.get('title')  # Get title from form
    if not title:
        flash('Enter title')
    task = ToDo.query.filter_by(email=current_user.email, title=title).first()  # Find requested task
    if task:
        db.session.delete(task)  # Delete task
        db.session.commit()
        return jsonify({'code': '200',
                        'response': 'OK'}), 200
    else:
        return jsonify({'code': '404',
                        'error': 'Not Found'}), 404

# Display all tasks for admin
@td_demo.route('/all_task', methods=['GET'])
def all_tasks():
    if current_user.is_authenticated and current_user.email == 'admin@a.com':
        cursor = ToDo.query.all()  # Collecting all tasks - only for admin
        all_task = [row.serialize() for row in cursor]  # Make sql row json compatible
        return jsonify({'code': '200',
                        'tasks': all_task}), 200
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Filter all tasks by status for admin
@td_demo.route('/all_task/status=<stat>')
def all_task_status(stat):
    if current_user.is_authenticated and current_user.email == 'admin@a.com':
        cursor = ToDo.query.filter_by(status=stat).all()  # Collect filtered tasks
        if cursor:
            tasks = [row.serialize() for row in cursor]  # Make sql row json compatible
            return jsonify({'code': '200',
                            'tasks': tasks}), 200
        else:
            return jsonify({'code': '404',
                            'error': 'Not Found'}), 404
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401

# Filter all tasks by title for admin
@td_demo.route('/all_task/title=<ttl>')
def all_task_title(ttl):
    if current_user.is_authenticated and current_user.email == 'admin@a.com':
        cursor = ToDo.query.filter_by(title=ttl).all()  # Collect filtered tasks
        if cursor:
            tasks = [row.serialize() for row in cursor]  # Make sql row json compatible
            return jsonify({'code': '200',
                            'tasks': tasks}), 200
        else:
            return jsonify({'code': '404',
                            'error': 'Not Found'}), 404
    else:
        return render_template('login.html', response='401: Unauthorised, Please Login'), 401
