from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from PIL import Image
import io
from sympy import preview, sympify
from sympy.parsing.latex import parse_latex
import base64
views = Blueprint('views', __name__)


def latexToImg(formula):
    expr = r"$${}$$".format((formula))          #parse_latex removed
    preview(expr, viewer='file', filename='temp.png', euler=False)
    image = Image.open('temp.png')
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    imageB = base64.b64encode(buffered.getvalue()).decode('ascii')
    return imageB

@views.route('/', methods=['GET', 'POST'])
@login_required                                     #install antlr4-python3-runtime==4.10
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML
        title = note.split("|")[0]
        formula = note.split("|")[1]
        explanation = note.split("|")[2] 
        #formatted_latex = r"\mathrm{{{}}}".format(note)
        imageB = latexToImg(formula)

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(title=title, user_id=current_user.id, encoded_image=imageB, explanation=explanation)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note ajoutée!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note supprimée!', category='success')
    return jsonify({})

@views.route('/modify-note', methods=['POST'])
def modify_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    new_title = note['new_title']
    new_explanation = note['new_explanation']
    new_latex = note['new_latex']
    note = Note.query.get(noteId)

    #re-parsing the latex code:

    imageB = latexToImg(new_latex)
    if note:
        if note.user_id == current_user.id:
            Note.query.filter_by(id=noteId).update({Note.title: new_title,Note.encoded_image: imageB, Note.explanation: new_explanation})
            db.session.commit()
            flash('Note modifiée!', category='success')
    return jsonify({})
