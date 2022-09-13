from typing import List
from flask import Flask, render_template, request, redirect, flash, session
from flask_wtf import FlaskForm
from flask_babel import Babel, _
from wtforms import SubmitField, SelectField, FileField, BooleanField
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha
from flask_sqlalchemy import SQLAlchemy
from copy import copy
from magic import from_buffer
import os
import io
import ctda
from models.result.error import ErrorResult
from models.result.successful import SuccessfulResult

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(12).hex()
    CAPTCHA_ENABLE = True
    CAPTCHA_LENGTH = 7
    CAPTCHA_WIDTH = 200
    CAPTCHA_HEIGHT = 60
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SESSION_TYPE = 'sqlalchemy'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


try:
    maxSize = int(os.environ['MAXSIZE'])
except Exception:
    maxSize = 300


class MainForm(FlaskForm):
    file = FileField(
        'Select file. Currently supported file types are CSV and Excel; maximum data size accepted has been set to ' + str(maxSize) + ' points.')
    maxdim = SelectField('Maximum dimension', choices=[
                         (2, '2'), (1, '1'), (0, '0')])
    coeff = SelectField('Field coefficient (7 is recommended for 3-dimensional data)',
                        choices=[(7, '7'), (3, '3'), (2, '2')])
    igLabels = BooleanField(
        'Ignore first row (check this if the first row contains, say, labels)')
    igEnum = BooleanField(
        'Ignore first column (check this if the first column contains, say, the enumeration index)')
    delimiter = SelectField('Delimiter (if applicable; the comma is the most common delimiter if unsure)', choices=[
                            (',', ','), (';', ';'), (':', ':'), (' ', ' '), ('|', '|'), ('\t', 'tab')])
    lineterminator = SelectField('Line terminator (if applicable; the new line is the most common line terminator if unsure)', choices=[
                                 ('\n', 'new line'), ('\n\n', 'double new line')])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config.from_object(Config)
Session(app)
captcha = FlaskSessionCaptcha(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="Home")


@app.route('/instructions', methods=['GET', 'POST'])
def instructions():
    return render_template('instructions.html', title="How to use the analyzer")


@app.route('/analyzer', methods=['GET', 'POST'])
def analyzer():
    form = MainForm()
    if form.submit.data:
        if captcha.validate():
            try:
                upload = form.file.data.read()
            except Exception:
                flash('Please select a file.')
                return render_template('analyzer.html', title="Analyzer", form=form)
            co = copy(upload)
            type = from_buffer(co).upper()
            if 'ASCII' in type or 'CSV' in type or 'TEXT' in type:
                t = 'csv'
                f = io.TextIOWrapper(io.BufferedReader(io.BytesIO(upload)))
            elif 'EXCEL' in type:
                t = 'xls'
                f = io.BufferedReader(io.BytesIO(upload))
            else:
                flash('File type not yet supported or file format error.')
                return render_template('analyzer.html', title="Analyzer", form=form)
            try:
                result = ctda.analyze(f, t, int(form.maxdim.data), int(
                    form.coeff.data), form.delimiter.data, form.lineterminator.data, form.igLabels.data, form.igEnum.data, maxSize)
                if isinstance(result, ErrorResult):
                    flash(result)
                    return render_template('analyzer.html', title="Analyzer", form=form)
                session['last_result'] = result.toJSON()
                return redirect('/analyzer/results')
            except Exception:
                flash('There seems to a miscalculation.')
                return render_template('analyzer.html', title="Analyzer", form=form)
        else:
            flash('Captcha incorrect.')
            return render_template('analyzer.html', title="Analyzer", form=form)
    return render_template('analyzer.html', title="Analyzer", form=form)


@app.route('/analyzer/results', methods=['GET'])
def analyzerResults():
    if 'last_result' in session:
        encoded = session['last_result']
    else:
        encoded = None
    result = SuccessfulResult.fromJson(encoded=encoded)
    return render_template(
        'results.html',
        title="Results",
        diagram=result.diagram,
        barcode=result.barcode,
        betti=result.betti,
        stats=result.stats,
        raw=result.dgms,
        dim=result.totald,
        latest_result=result.toJSON()
    )


@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')
