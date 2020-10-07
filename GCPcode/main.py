from flask import Flask, render_template, url_for, request, redirect

from nba_api.stats.static import players, teams

from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster

import pymongo

from pymongo import MongoClient

import numpy as np

#chase username and password accordingly
try:
    client = pymongo.MongoClient("mongodb+srv://Bibartan:bibpass@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
    print("Connected")
except:
    print("Not connected")

app = Flask(__name__)

client_year = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Years?retryWrites=true&w=majority")
client_trade = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
client_teams = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Teams?retryWrites=true&w=majority")
client_franLeaders = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Franchise_Leaders?retryWrites=true&w=majority")
client_coaches = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Coaches?retryWrites=true&w=majority")

@app.route('/')

def root():

    return render_template('index.html')





@app.route('/AboutPage')

def AboutPage():
    return render_template('about.html')

@app.route('/Players', methods=['GET', 'POST'])
def Players():
    players_db = client['Players']
    NBA = players_db['NBA_selected']
    players = []
    for player in NBA.find():
        players.append(player)
    players = sorted(players, key=lambda k: k['Name'])

    if request.method == 'POST':
        filter_status = request.form['Filter by status']
        if filter_status != "All statuses":
            players_with_status = []
            for player in players:
                if player['Status'] == filter_status:
                    players_with_status.append(player)
            players=players_with_status

        filter_position = request.form['Filter by position']
        if filter_position != "All positions":
            players_in_position = []
            for player in players:
                if player['Position'] == filter_position:
                    players_in_position.append(player)
            players=players_in_position

        filter_team = request.form['Filter by team']
        if filter_team != "All teams":
            players_in_team = []
            for player in players:
                if player['Team'] == filter_team:
                    players_in_team.append(player)
            players=players_in_team

        sort = request.form['Sort']
        if sort == "Name (Z-A)":
            players = sorted(players, key=lambda k: k['Name'], reverse=True)
        elif sort == "Start Year (Earliest to Latest)":
            players = sorted(players, key=lambda k: k['Start Year'])
        elif sort == "Start Year (Latest to Earliest)":
            players = sorted(players, key=lambda k: k['Start Year'], reverse=True)
        elif sort == "End Year (Earliest to Latest)":
            players = sorted(players, key=lambda k: k['End Year'])
        elif sort == "End Year (Latest to Earliest)":
            players = sorted(players, key=lambda k: k['End Year'], reverse=True)
        return render_template('players.html', players=players, filter_status=filter_status, filter_position=filter_position, filter_team=filter_team, sort=sort)
    else: 
        return render_template('players.html', players=players, filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')

@app.route('/Teams', methods=['GET', 'POST'])
def Teams():
    teams_db = client['Teams']
    NBA = teams_db['NBA']
    WNBA = teams_db['WNBA']
    teams = []
    for team in NBA.find():
        teams.append(team)
    for team in WNBA.find():
        teams.append(team)
    teams = sorted(teams, key=lambda k: k['Name'])

    if request.method == 'POST':
        filter_league = request.form['Filter by league']
        if filter_league != "All leagues":
            teams_in_league = []
            for team in teams:
                if team['League'] == filter_league:
                    teams_in_league.append(team)
            teams=teams_in_league

        filter_conference = request.form['Filter by conference']
        if filter_conference != "All conferences":
            league = filter_conference.split(" ")[0]
            conference = filter_conference.split(" ")[1]
            teams_in_conference = []
            for team in teams:
                if team['League'] == league and team['Conference'] == conference:
                    teams_in_conference.append(team)
            teams=teams_in_conference

        filter_division = request.form['Filter by division']
        if filter_division != "All divisions":
            teams_in_division = []
            for team in teams:
                if team['League'] == 'NBA':
                    if team['Division'] == filter_division:
                        teams_in_division.append(team)
            teams=teams_in_division


        sort = request.form['Sort'] 
        if sort == "Team Name (Z-A)":
            teams = sorted(teams, key=lambda k: k['Name'], reverse=True) 
        elif sort == "Location (A-Z)":
            teams = sorted(teams, key=lambda k: k['Location']) 
        elif sort == "Location (Z-A)":
            teams = sorted(teams, key=lambda k: k['Location'], reverse=True) 
        elif sort == "Year Founded (Earliest to Latest)":
            teams = sorted(teams, key=lambda k: k['Year Founded']) 
        elif sort == "Year Founded (Latest to Earliest)":
            teams = sorted(teams, key=lambda k: k['Year Founded'], reverse=True) 
        return render_template('teams.html', teams=teams, filter_league=filter_league, filter_conference=filter_conference, filter_division=filter_division, sort=sort)
    else:
        return render_template('teams.html', teams=teams, filter_league="All leagues", filter_conference="All conferences", filter_division="All divisions", sort='Default: Team Name (A-Z)')



@app.route('/News', methods=['GET', 'POST'])
def News():
    news_db = client['News']
    NBA = news_db['NBA']
    articles = []
    for article in NBA.find():
        articles.append(article)
    articles = sorted(articles, key=lambda k: k['Updated'], reverse=True) 
    if request.method == 'POST':
        filter_category = request.form['Filter by category']
        if filter_category != "All categories":
            articles_in_category = []
            for article in articles:
                if article['Categories'] == filter_category:
                    articles_in_category.append(article)
            articles=articles_in_category

        filter_team = request.form['Filter by team']
        if filter_team != "All teams":
            articles_for_team = []
            for article in articles:
                if article['Team'] == filter_team:
                    articles_for_team.append(article)
            articles=articles_for_team

        sort = request.form['Sort'] 
        if sort == "Date (Earliest to Latest)":
            articles = sorted(articles, key=lambda k: k['Updated']) 
        elif sort == "Title (A to Z)":
            articles = sorted(articles, key=lambda k: k['Title']) 
        elif sort == "Title (Z to A)":
            articles = sorted(articles, key=lambda k: k['Title'], reverse=True) 
        elif sort == "Source (A to Z)":
            articles = sorted(articles, key=lambda k: k['OriginalSource']) 
        elif sort == "Source (Z to A)":
            articles = sorted(articles, key=lambda k: k['OriginalSource'], reverse=True)
        return render_template('news.html', articles=articles, filter_category=filter_category, filter_team=filter_team, sort=sort)
    else:
        return render_template('news.html', articles=articles, filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")

@app.route('/Year', methods=['GET', 'POST'])
def Year():

    db_year = client_year['Years']
    collection_year = db_year['NBA']
    year_info_documents = []
    for document in collection_year.find():
        year_info_documents.append(document)
    return render_template('year.html',year_info_documents=year_info_documents)

@app.route('/Franchise_Leaders')

def record():

    db_franLeaders = client_franLeaders['Franchise_Leaders']
    collection_franLeaders = db_franLeaders['NBA']
    franLeaders_documents = []
    for document in collection_franLeaders.find():
        franLeaders_documents.append(document)
    
    return render_template('franchiseLeaders.html',franLeaders_documents=franLeaders_documents)


@app.route('/Coaches',methods = ['GET','POST'])

def coaches():

    db_coaches = client_coaches['Coaches']
    collection_coaches = db_coaches['NBA']
    coaches_documents = []
    for document in collection_coaches.find():
        coaches_documents.append(document)

    return render_template('coaches.html',coaches_documents=coaches_documents)





@app.route('/Settings')

def Settings():

    return render_template('settings.html')


@app.route('/favteam', methods=['GET', 'POST'])
def favteam():
    teamList = teams.get_teams()
    if request.method == 'POST':
        team = request.form['teamchoices']
        if team == "":
            return render_template('favteam.html', teamList = teamList)

        addTeam = teams.find_teams_by_full_name(team)
        id = addTeam[0].get('id')
        teamBackground = teamdetails.TeamDetails(id).get_normalized_dict().get('TeamBackground')[0]
        teamSocial = teamdetails.TeamDetails(id).get_normalized_dict().get('TeamSocialSites')
        teamHeaders = teaminfocommon.TeamInfoCommon(id).team_info_common.get_dict()['headers']
        teamData = teaminfocommon.TeamInfoCommon(id).team_info_common.get_dict()['data']

        abr = teamBackground.get('ABBREVIATION')
        nickname = teamBackground.get('NICKNAME')
        city = teamBackground.get('CITY')
        state = addTeam[0].get('state')
        year = teamBackground.get('YEARFOUNDED')
        coach = teamBackground.get('HEADCOACH')
        manager = teamBackground.get('GENERALMANAGER')
        facebook = teamSocial[0].get('WEBSITE_LINK')
        instagram = teamSocial[1].get('WEBSITE_LINK')
        twitter = teamSocial[2].get('WEBSITE_LINK')
        conference = teamData[0][teamHeaders.index('TEAM_CONFERENCE')]




        return render_template('favteam.html', teamList=teamList, name=team, abr=abr, nickname=nickname, city=city, state=state, year=year, facebook=facebook, instagram=instagram, twitter=twitter, coach=coach, manager=manager, conference=conference)
    else:
        return render_template('favteam.html', teamList=teamList)


@app.route('/favplayer', methods=['GET', 'POST'])
def favplayer():
    playerList = players.get_players()
    if request.method == 'POST':
        person = request.form['playerchoices']
        if person == "":
            return render_template('favplayer.html', playerList = playerList)

        addPlayer = players.find_players_by_full_name(person)
        id = addPlayer[0].get('id')
        playerInfo = commonplayerinfo.CommonPlayerInfo(id).get_normalized_dict().get('CommonPlayerInfo')[0]
        name = addPlayer[0].get('full_name')
        if addPlayer[0].get('is_active') == "true":
            active ='active'
        else:
            active = 'inactive'

        yearsActive = int(playerInfo.get('TO_YEAR'))-int(playerInfo.get('FROM_YEAR'))
        teamName = playerInfo.get('TEAM_NAME')
        teamCity = playerInfo.get('TEAM_CITY')
        jersey = playerInfo.get('JERSEY')
        position = playerInfo.get('POSITION')
        height = playerInfo.get('HEIGHT')
        weight = playerInfo.get('WEIGHT')
        draftYear = playerInfo.get('DRAFT_YEAR')
        draftRound = playerInfo.get('DRAFT_ROUND')
        draftNumber = playerInfo.get('DRAFT_NUMBER')
        birth = playerInfo.get('BIRTHDATE')
        school = playerInfo.get('SCHOOL')
        PTS = playerInfo.get('PTS')
        AST = playerInfo.get('AST')
        REB = playerInfo.get('REB')


        return render_template('favplayer.html', playerList = playerList, addPlayer = addPlayer, name=name, active=active, yearsActive= yearsActive, teamName=teamName, teamCity=teamCity, jersey = jersey, position=position, height=height, weight=weight, draftYear=draftYear, draftRound=draftRound, draftNumber=draftNumber, birth=birth, school=school, PTS=PTS, AST=AST, REB=REB)
    else:
        return render_template('favplayer.html', playerList = playerList)





@app.route('/comparison')

def comparison():

    if request.method == 'POST':

        pass

    else:

        return render_template('comparison.html')





@app.route('/account')

def account():

    return render_template('login.html')





@app.route('/pop-up')

def popup():

    pass



if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

