from datetime import datetime

from flask import render_template, flash, redirect, request, url_for, current_app, g
from flask_login import current_user, login_required

from app import db
from app.main import bp
from app.main.forms import EditProfileForm, NoteForm, IPForm, SearchForm
from app.models import User, Notes, IntellectualProperty


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def game_home():
    avail_ips = IntellectualProperty.query.order_by(IntellectualProperty.estimated_value.desc())
    form = NoteForm()
    if form.validate_on_submit():
        note = Notes(body=form.note.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        flash("Noted!")
        return redirect(url_for('main.game_home'))
    page = request.args.get('page', 1, type=int)
    notes = current_user.followed_notes().paginate(page, current_app.config['NOTES_PER_PAGE'], False)
    next_url = url_for('main.game_home', page=notes.next_num) if notes.has_next else None
    prev_url = url_for('main.game_home', page=notes.prev_num) if notes.has_prev else None
    return render_template(
        'index.html',
        title='Welcome',
        form=form,
        ips=avail_ips,
        notes=notes.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.favorite_ip = form.favorite_ip.data
        db.session.commit()
        flash('Saved your changes, sir.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.favorite_ip.data = current_user.favorite_ip
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/user/<username>')
@login_required
def user(username):
    user_for_page = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    notes = Notes.query.filter_by(user_id=user_for_page.id).order_by(Notes.timestamp.desc()).paginate(
        page, current_app.config['NOTES_PER_PAGE'], False)
    next_url = url_for('main.user', username=user_for_page.username, page=notes.next_num) if notes.has_next else None
    prev_url = url_for('main.user', username=user_for_page.username, page=notes.prev_num) if notes.has_prev else None
    return render_template('user.html', user=user_for_page, notes=notes.items, next_url=next_url, prev_url=prev_url)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect((url_for('main.game_home')))
    if user == current_user:
        flash("Can't follow yourself, dummy")
        redirect(url_for('main.game_home'))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following this bloke: {}'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Can not find em: {}'.format(username))
        redirect(url_for('main.game_home'))
    if user == current_user:
        flash('Why you wanna unfollow yourself?')
        redirect(url_for('main.game_home'))
    current_user.unfollow(user)
    db.session.commit()
    flash('Stopped following this one: {}'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/global_hub')
def global_hub():
    """Where a user can find all other users."""
    page = request.args.get('page', 1, type=int)
    notes = Notes.query.order_by(Notes.timestamp.desc()).paginate(page, current_app.config['NOTES_PER_PAGE'], False)
    next_url = url_for('main.global_hub', page=notes.next_num) if notes.has_next else None
    prev_url = url_for('main.global_hub', page=notes.prev_num) if notes.has_prev else None
    return render_template('index.html', title='Global Hub', notes=notes.items, next_url=next_url, prev_url=prev_url)


@bp.route('/new_ip', methods=['GET', 'POST'])
@login_required
def new_ip():
    form = IPForm()
    if form.validate_on_submit():
        ip = IntellectualProperty(
            name=form.name.data,
            description=form.description.data,
            clout=form.clout.data,
            estimated_value=form.estimated_value.data)
        db.session.add(ip)
        db.session.commit()
        flash('A new Intellectual Property has come into the world: {}'.format(form.name.data))
        return redirect(url_for('main.game_home'))
    return render_template('new_ip.html', title='Create Your New IP', form=form)


@bp.route('/ip/<ip_id>')
@login_required
def ip_details(ip_id):
    ip_for_page = IntellectualProperty.query.filter_by(id=ip_id).first_or_404()
    return render_template('ip_details.html', ip=ip_for_page)


@bp.route('/ip/<ip_name>/popup')
@login_required
def ip_popup(ip_name):
    ip_for_page = IntellectualProperty.query.filter_by(name=ip_name).first_or_404()
    return render_template('ip_popup.html', ip=ip_for_page)


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.global_hub'))
    page = request.args.get('page', 1, type=int)
    print('the notes per page')
    print(current_app.config['NOTES_PER_PAGE'])
    notes, total = Notes.search(g.search_form.q.data, page, current_app.config['NOTES_PER_PAGE'])
    print('these are the notes')
    print(notes)
    next_url = url_for('main.search', q=g.search_form.q.data, page= page + 1) \
        if total > page * current_app.config['NOTES_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page= page - 1) if page > 1 else None
    return render_template('search.html', title='Search', notes=notes, next_url=next_url, prev_url=prev_url)
