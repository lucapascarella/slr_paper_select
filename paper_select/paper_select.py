from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from paper_select.db import get_db

bp = Blueprint('paper_select', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session and session['user'] is not None:
        return redirect(url_for('paper_select.check'))  # go to check page
    if request.method == 'POST':
        if request.form['user']:
            session['user'] = request.form['user']
            flash('You were logged in, ' + session['user'])
            return redirect(url_for('paper_select.check'))
    return redirect(url_for('paper_select.index'))


@bp.route('/clear_session')
def clear_session():
    if 'user' in session and session['user'] is not None:
        session.pop('user')
    return redirect(url_for('paper_select.index'))


@bp.route('/charts')
def chart():
    db = get_db()
    cur = db.execute('select author, count(id) as cnt from remark '
                     'group by author order by cnt desc limit 20;')
    winners = cur.fetchall()
    return render_template('chart.html', winners=winners)


@bp.route('/check')
def check():
    if 'user' in session:
        db = get_db()
        data = {}
        query = """
                   select author, count(id) as cnt from remark
                   where author ='%s';
                """ % (session['user'])
        cur = db.execute(query)
        (current_author, author_count) = cur.fetchone()
        data['count'] = author_count
        query = """
            select id, csv_id, title, authors, abstract, venue, year, doi, source from paper 
            where id not in (select paper_id from remark) 
            limit 1;
        """
        cur = db.execute(query)
        paper = cur.fetchone()
        if paper is not None:
            (id, csv_id, title, authors, abstract, venue, year, doi, source) = paper
            print("Checking {} {}".format(id, title))
            data['paper'] = {'id': id, 'csv_id': csv_id, 'title': title, 'authors': authors, 'abstract': abstract, 'venue': venue, 'year': year, 'doi': doi, 'source': source}
        else:
            data['paper'] = None
        return render_template('check.html', data=data)
    else:
        return render_template('home.html')


@bp.route('/save_result', methods=['GET', 'POST'])
def save_result():
    if request.method == 'POST':
        db = get_db()
        data = request.form.to_dict()
        # print(data)

        paper_id = data['paper_id']
        acceptance = int(data['selection'])
        if acceptance == 3:
            return redirect(url_for('paper_select.check'))
        exclusion_note_list = []

        if 'inclusion_note' in data:
            inclusion_note = data['inclusion_note']
        else:
            inclusion_note = ''

        if 'note_not_full' in data:
            exclusion_note_list.append(data['note_not_full'])
        if 'note_not_related' in data:
            exclusion_note_list.append(data['note_not_related'])
        if 'note_talks_pretrained_models' in data:
            exclusion_note_list.append(data['note_talks_pretrained_models'])
        if 'note_talks_word_embeddings' in data:
            exclusion_note_list.append(data['note_talks_word_embeddings'])
        if 'other_option' in data and data['other_option'] != '':
            exclusion_note_list.append(data['other_option'])

        exclusion_note = '|'.join(exclusion_note_list)
        insert = (paper_id, session['user'], acceptance, inclusion_note, exclusion_note)
        db.execute('insert into remark (paper_id, author, acceptance, inclusion_note, exclusion_note) values (?, ?, ?, ?, ?)', insert)
        db.commit()
        return redirect(url_for('paper_select.check'))
    return redirect(url_for('paper_select.index'))
