from flask import Flask, render_template, url_for, request, redirect

from nba_api.stats.static import players, teams

from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster

import pymongo

from pymongo import MongoClient

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

@app.route('/')

def root():

    return render_template('index.html')





@app.route('/AboutPage')

def AboutPage():
    return render_template('about.html')

@app.route('/Players', methods=['GET', 'POST'])
def Players():
    db = client['Players']
    collection = db['NBA_selected']
    player_info_documents = []
    for document in collection.find():
        player_info_documents.append(document)
    return render_template('players.html', player_info_documents=player_info_documents)

@app.route('/Teams', methods=['GET', 'POST'])
def Teams():
    db = client['Teams']
    collection = db['NBA']
    collection_2 = db['WNBA']
    nba_docs = []
    for document in collection.find():
        nba_docs.append(document)

    collection_2 = db['WNBA']
    wnba_docs = []
    for document in collection_2.find():
        wnba_docs.append(document)
    return render_template('teams.html', nba_docs=nba_docs, wnba_docs=wnba_docs)



@app.route('/News', methods=['GET', 'POST'])
def News():
    if request.method == 'POST':
        pass
    else:
        return render_template('news.html')

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

def TradeSim():

    return render_template('coaches.html')





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

