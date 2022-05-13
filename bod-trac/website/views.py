from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import current_user
from .models import BodyWeight, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html', currentUser=current_user)


@views.route('/add', methods=['POST'])
def add_weight():
    currentWeight = request.form.get('currentWeight')
    if currentWeight:
        newBodyweight = BodyWeight(bW=currentWeight, user_id=current_user.id)
        db.session.add(newBodyweight)
        db.session.commit()

        label = []
        weight = []

        for recordedBw in current_user.recordedBws:
            label.append(json.dumps(recordedBw.currentDate.strftime('%d %b')))
            weight.append(json.dumps(float(recordedBw.bW)))

        flash('Weight updated', category='success')
        return render_template('account.html', currentUser=current_user, label=label, weight=weight)
    else:
        label = []
        weight = []

        for recordedBw in current_user.recordedBws:
            label.append(json.dumps(recordedBw.currentDate.strftime('%d %b')))
            weight.append(json.dumps(float(recordedBw.bW)))

        flash('No weight entered', category='error')
        return render_template('account.html', currentUser=current_user, label=label, weight=weight)


@views.route('/deleteWeight', methods=['POST'])
def delete_weight():
    chosenWeight = json.loads(request.data)
    weight = chosenWeight['id']
    getWeight = BodyWeight.query.get(weight)
    if getWeight:
        if getWeight.user_id == current_user.id:
            db.session.delete(getWeight)
            db.session.commit()
    return jsonify({})


@views.route('/updateStartingBw', methods=['POST'])
def update_starting_weight():
    newstartingBw = request.form.get('startingBw')

    if newstartingBw:
        currentStartingBw = User.query.filter(User.id == current_user.id).one()
        currentStartingBw.startingBw = newstartingBw
        db.session.commit()

    label = []
    weight = []

    for recordedBw in current_user.recordedBws:
        label.append(json.dumps(recordedBw.currentDate.strftime('%d %b')))
        weight.append(json.dumps(float(recordedBw.bW)))
        
    flash('Updated starting bodyweight', category='success')
    return render_template('account.html', currentUser=current_user, label=label, weight=weight)
    
