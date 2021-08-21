from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User

from flask_app.models.show import Show



@app.route('/shows')
def exam_index():
    if 'user_id' not in session:
        flash('Please log in to view this page')
        return redirect('/')
    shows = Show.get_all_shows()
    print(shows)
    
    return render_template('shows.html', shows = shows)

@app.route('/shows/new')
def new_show():
    return render_template('new_show.html')


@app.route('/shows/create', methods=['POST'])
def create_recipe():
    
    if Show.validate_show(request.form):
        data = {
            'title' : request.form['title'],
            'network' : request.form['network'],
            'date' : request.form['date'],
            'description' : request.form['description'],
            'users_id' : session['user_id']
        }
        Show.create_show(data)
    #     print('show valid')
    #     return redirect('/shows')
    # print('show not valid')
    
    return redirect('/shows/new')


@app.route('/info/shows/')
def info_show():
    shows = Show.get_all_shows()
    return render_template('shows.html', shows = shows)


@app.route('/shows/<int:show_id>')
def show_info(show_id):
    
    show = Show.get_show_by_id({'id' : show_id})
    
    return render_template('show_info.html', show = show)


@app.route('/shows/<int:show_id>/edit')
def edit_show(show_id):
    
    show = Show.get_show_by_id({'id' : show_id})
    
    return render_template('edit_show.html', show = show)


@app.route('/shows/<int:show_id>/update', methods=['POST'])
def update_show(show_id):
    if Show.validate_show(request.form):
        data = {
            'title' : request.form['title'],
            'network' : request.form['network'],
            'date' : request.form['date'],
            'description' : request.form['description'],        
            'id' : show_id
        }
        Show.update_show(data)
        
    return redirect(f'/shows/{show_id}')



@app.route('/shows/<int:show_id>/like')
def like_show(show_id):
    show = Show.get_show_by_id({'id' : show_id})
    
    return render_template('show_info.html', show = show)


