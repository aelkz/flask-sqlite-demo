from app import (
    app,
)
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    g
)
from app.forms import (
    AddLectureForm,
    AddExecutionForm,
    AddExamForm
)
from app.query_helper import (
    query_db,
    insert
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/vorlesung', methods=('GET', 'POST'))
def add_lecture():
    form = AddLectureForm()

    if form.validate_on_submit():
        insert('lecture',
               ('name', 'shortcut', 'ects'),
               (form.name.data, form.shortcut.data, form.ects.data))

        flash("Vorlesung erfolgreich erstellt!")
        return redirect(url_for('add_lecture'))

    return render_template('add_lecture.html',
                           title="Vorlesungen",
                           form=form
                           )


@app.route('/view_pruefungen', methods=('GET', 'POST'))
def view_exams():
    exams = query_db(
        "select shortcut, name, semester, n_tries, mark, degree,kind  "
        "from exam natural join lecture limit 20")
    return render_template('view_exams.html',
                           exams=exams,
                           )


@app.route('/pruefung', methods=('GET', 'POST'))
def add_exam():
    form = AddExamForm()
    executions = query_db("select shortcut, semester from execution")
    form.executions.choices = [('?'.join(map(str, k)), "{} in Semester {}".format(*k)) for k in executions]

    if form.validate_on_submit():
        shortcut, semester = form.executions.data.split('?')
        if len(query_db("select 1 from exam where shortcut=? and semester=? and n_tries=?",
                        (shortcut, semester, form.n_tries.data))) > 0:
            flash("Prüfung existiert bereits!")
            return redirect(url_for('add_exam'))

        insert('exam',
               ('shortcut', 'semester', 'n_tries', 'mark', 'degree', 'kind'),
               (shortcut, semester, form.n_tries.data, form.mark.data,
                form.degree.data,
                form.kind.data))

        flash("Prüfungs erfolgreich erstellt!")
        return redirect(url_for('add_exam'))

    return render_template('add_exam.html',
                           title="Prüfungen",
                           form=form
                           )


@app.route('/durchfuehrung', methods=('GET', 'POST'))
def add_execution():
    form = AddExecutionForm()
    lectures = query_db("select shortcut,name from lecture")
    form.shortcut.choices = [(k[0], k[1]) for k in lectures]

    if form.validate_on_submit():
        # insert
        insert('execution',
               ('shortcut', 'lecturer', 'semester'),
               (form.shortcut.data, form.lecturer.data, form.semester.data))
        flash("Durchführung erfolgreich erstellt!")
        return redirect(url_for('add_execution'))

    return render_template('add_execution.html',
                           title="Durchführung",
                           form=form)


# administration

@app.teardown_appcontext
def close_connection(exception):
    """
    after each request close active database connection
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
