from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange

class GenForm(FlaskForm):
    example = "Du bist ein Mathematik-Tutor, beantworte deshalb nur Fragen zu Mathematik. Halte deine Antworten kurz. Wenn andere Fragen gestellt werden oder die Frage nicht mit dem Jugendschutz vereinbar ist, antworte: 'Ich kann diese Frage nicht beantworten.'"
    #api_key = StringField('API-Key von OpenAI: ', validators=[DataRequired()])
    context = TextAreaField('Kontextinformationen (hier mit Beispieltext):',
                            [validators.optional(), validators.length(max=10000)], default=example, render_kw={"rows": 7})
    pdf_upload = FileField('PDF-Datei auswählen', validators=[DataRequired()])
    submit = SubmitField('Generiere Link')

class GenPicForm(FlaskForm):
    example = "Die Eingabe muss über Dinosaurier handeln und mit dem Jugendschutz vereinbar sein."
    # api_key = StringField('API-Key von OpenAI: ', validators=[DataRequired()])
    context = TextAreaField('Bedingung (hier mit Beispieltext):',
                            [validators.optional(), validators.length(max=10000)], default=example, render_kw={"rows": 7})
    vals = IntegerField('Anzahl Links (max. 33):',[validators.DataRequired(), NumberRange(min=1, max=33)])
    submit = SubmitField('Generiere Links')
