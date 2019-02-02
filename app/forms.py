from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError
)
from app import query_db


class AddLectureForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 1024)])
    shortcut = StringField('Kürzel', validators=[DataRequired(), Length(1, 64)])
    ects = IntegerField('ECTS', default=1, validators=[DataRequired()])
    submit = SubmitField('Erstellen')

    def validate_shortcut(self, shortcut):
        if len(query_db("select * from lecture where shortcut= ? ", (shortcut.data,))) > 0:
            raise ValidationError("Dieses Kürzel existiert bereits!")


class AddExecutionForm(FlaskForm):
    shortcut = SelectField('Kürzel', coerce=str, validators=[DataRequired()])
    lecturer = StringField('Dozent', validators=[DataRequired()])
    semester = IntegerField('Semester', default=1, validators=[DataRequired()])
    submit = SubmitField('Erstellen')


class AddExamForm(FlaskForm):
    executions = SelectField('Durchführung', coerce=str, validators=[DataRequired()])
    n_tries = IntegerField('Versuch', default=1, validators=[DataRequired()])
    mark = IntegerField('Note', validators=[DataRequired()])
    degree = SelectField('Abschluss', default='b', choices=[('b', 'Bachelor'), ('m', 'Master')])
    kind = SelectField('Art', coerce=int, default=0, choices=[(0, 'Schriftlich'), (1, 'Mündlich')])
    submit = SubmitField('Erstellen')
