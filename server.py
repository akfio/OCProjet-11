import json
from flask import Flask, render_template, request, redirect, flash, url_for
import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)
    except:
        flash("Sorry, that email was not found.")
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    competition_date = datetime.datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S')
    actual_date = datetime.datetime.now()
    valid_competition = competition_date > actual_date
    if valid_competition == True:
        if foundClub:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("COMPETITION OVER")
        return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash('PAS PLUS DE 12 PLACES PAR CLUB')
    elif placesRequired > int(club['points']):
        flash('PAS ASSEZ DE POINTS DISPONIBLE')
    else:
        club['points'] = int(club['points']) - placesRequired
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, clubs=clubs)


@app.route('/points')
def points_display():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
