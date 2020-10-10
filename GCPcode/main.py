from flask import Flask, render_template, url_for, request, redirect

import nba_api

from nba_api.stats.static import players, teams

from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster

import pymongo

from pymongo import MongoClient

import numpy as np

import requests

import time

import http.client

import json

import random

#chase username and password accordingly

# try:
client = pymongo.MongoClient("mongodb+srv://Bibartan:bibpass@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
#     print("Connected")
# except:
#     print("Not connected")


app = Flask(__name__)

# client_year = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Years?retryWrites=true&w=majority")
# client_trade = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
# client_teams = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Teams?retryWrites=true&w=majority")
# client_franLeaders = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Franchise_Leaders?retryWrites=true&w=majority")
# client_coaches = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Coaches?retryWrites=true&w=majority")


# get game information #
# client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/GAMES?retryWrites=true&w=majority")


@app.route('/')
def root(method=['GET']):
    #five_random_games = []
    #five_games_info = []
    #gamedb = client["GAMES"]
    #gamecol = gamedb["NBA2019"]

    # get 5 random games #
    #for i in range(5):
    #    randomgame = random.randrange(1061)
    #    five_random_games.append(randomgame)
    #    game_info = []
    #    gamedoc = gamecol.find_one({"_id":randomgame})
    #    game_info.append(gamedoc["HomePoints"])
    #    game_info.append(gamedoc["HomeTeam"])
    #    game_info.append(gamedoc["AwayPoints"])
    #    game_info.append(gamedoc["AwayTeam"])
    #    five_games_info.append(game_info)

    return render_template('home.html')



@app.route('/AboutPage')
def AboutPage():
    return render_template('about.html')

@app.route('/AdrianDantley')
def AdrianDantley():
    player_1 = {
        "Name": "Adrian Dantley",
        "Status": "Not Active",
        "Team": "Jazz",
        "Position": "Forward",
        "Start Year": "1976",
        "End Year": "1990"
    };
    players = []
    players.append(player_1)
    return render_template('adriandantley.html', players=players)

@app.route('/AlexEnglish')
def AlexEnglish():
    player_1 = {
        "Name": "Alex English",
        "Status": "Not Active",
        "Team": "Nuggets",
        "Position": "Forward",
        "Start Year": "1976",
        "End Year": "1990"
    };
    players = []
    players.append(player_1)
    return render_template('alexenglish.html', players=players)

@app.route('/AllenIverson')
def AllenIverson():
    player_1 = {
        "Name": "Allen Iverson",
        "Status": "Not Active",
        "Team": "76ers",
        "Position": "Guard",
        "Start Year": "1996",
        "End Year": "2009"
    };
    players = []
    players.append(player_1)
    return render_template('alleniverson.html', players=players)

@app.route('/Players', methods=['GET', 'POST'])
def Players():
    player_1 = {
        "Name": "Adrian Dantley",
        "Status": "Not Active",
        "Team": "Jazz",
        "Position": "Forward",
        "Start Year": "1976",
        "End Year": "1990"
    };

    player_2 = {
        "Name": "Alex English",
        "Status": "Not Active",
        "Team": "Nuggets",
        "Position": "Forward",
        "Start Year": "1976",
        "End Year": "1990"
    };

    player_3 = {
        "Name": "Allen Iverson",
        "Status": "Not Active",
        "Team": "76ers",
        "Position": "Guard",
        "Start Year": "1996",
        "End Year": "2009"
    };

    players = []
    players.append(player_1)
    players.append(player_2)
    players.append(player_3)

    return render_template('players.html', players=players, num_instances=len(players), filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')

    '''
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
        return render_template('players.html', players=players, num_instances=len(players), filter_status=filter_status, filter_position=filter_position, filter_team=filter_team, sort=sort)
    else: 
        return render_template('players.html', players=players, num_instances=len(players), filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')
'''
@app.route('/Players_search', methods=['GET', 'POST'])
def Players_search():
    players = []
    if request.method == 'POST':
        players_db = client['Players']
        NBA = players_db['NBA_selected']
        if request.form['submit'] == 'Search':
            search = request.form['search']
            for player in NBA.find():
                if player['Name'] == search:
                    players.append(player)
        else:
            for player in NBA.find():
                players.append(player)
            players = sorted(players, key=lambda k: k['Name'])
    return render_template('players.html', players=players, num_instances=len(players), filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')
    
@app.route('/Teams', methods=['GET', 'POST'])
def Teams():
    team_1 = {
        "Name": "Hawks",
        "League": "NBA",
        "Location": "Atlanta",
        "Year Founded": "1949",
        "Conference" : "East",
        "Division": "Southeast",
        "Coach": "Lloyd Pierce"
    };

    team_2 = {
        "Name": "Celtics",
        "League": "NBA",
        "Location": "Boston",
        "Year Founded": "1946",
        "Conference" : "East",
        "Division": "Atlantic",
        "Coach": "Brad Stevens"
    };

    team_3 = {
        "Name": "Nets",
        "League": "NBA",
        "Location": "Brooklyn",
        "Year Founded": "1976",
        "Conference" : "East",
        "Division": "Atlantic",
        "Coach": "Steve Nash"
    };

    teams = []
    teams.append(team_1)
    teams.append(team_2)
    teams.append(team_3)
    return render_template('teams.html', teams=teams, num_instances=len(teams), filter_league="All leagues", filter_conference="All conferences", filter_division="All divisions", sort='Default: Team Name (A-Z)')

    '''
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
        return render_template('teams.html', teams=teams, num_instances=len(teams), filter_league=filter_league, filter_conference=filter_conference, filter_division=filter_division, sort=sort)
    else:
        '''
@app.route('/Teams_search', methods=['GET', 'POST'])
def Teams_search():
    teams = []
    if request.method == 'POST':
        teams_db = client['Teams']
        NBA = teams_db['NBA']
        WNBA = teams_db['WNBA']
        if request.form['submit'] == 'Search':
            search = request.form['search']
            for team in NBA.find():
                if team['Name'] == search:
                    teams.append(team)
            for team in WNBA.find():
                if team['Name'] == search:
                    teams.append(team)
        else:
            for team in NBA.find():
                teams.append(team)
            for team in WNBA.find():
                teams.append(team)
            teams = sorted(teams, key=lambda k: k['Name'])
    return render_template('teams.html', teams=teams, num_instances=len(teams), filter_league="All leagues", filter_conference="All conferences", filter_division="All divisions", sort='Default: Team Name (A-Z)')
    
@app.route('/News', methods=['GET', 'POST'])
def News():
    news_1 = {
        "Updated": "2020-10-07",
        "Title": "Bam Adebayo Will Officially Return For Game 4",
        "Categories": "Injuries",
        "Team": "MIA",
        "OriginalSource": "Tim Reynolds",
        "OriginalSourceUrl": "https://twitter.com/ByTimReynolds/status/1313626888347291653"
    };

    news_2 = {
        "Updated": "2020-10-06",
        "Title": "Bam Adebayo Likely To Return In Game 4",
        "Categories": "Injuries",
        "Team": "MIA",
        "OriginalSource": "Adrian Wojnarowski",
        "OriginalSourceUrl": "https://twitter.com/wojespn/status/1313576977358520321?s=20"
    };

    news_3 = {
        "Updated": "2020-10-02",
        "Title": "Goran Dragic Ruled Out For Game 2",
        "Categories": "Injuries",
        "Team": "MIA",
        "OriginalSource": "Shams Charania",
        "OriginalSourceUrl": "https://twitter.com/ShamsCharania/status/1312149052654379008"
    }

    articles = []
    articles.append(news_1)
    articles.append(news_2)
    articles.append(news_3)
    return render_template('news.html', articles=articles, num_instances=len(articles), filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")

    '''
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
        return render_template('news.html', articles=articles, num_instances=len(articles), filter_category=filter_category, filter_team=filter_team, sort=sort)
    else:
        return render_template('news.html', articles=articles, num_instances=len(articles), filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")
'''
@app.route('/newsInstance1', methods=['GET', 'POST'])
def newsInstance_one():
    
    return render_template('news1.html')

@app.route('/newsInstance2', methods=['GET', 'POST'])
def newsInstance_two():
    
    return render_template('news2.html')

@app.route('/newsInstance3', methods=['GET', 'POST'])
def newsInstance_three():
    
    return render_template('news3.html')

@app.route('/News_search', methods=['GET', 'POST'])
def News_search():
    articles = []
    if request.method == 'POST':
        news_db = client['News']
        NBA = news_db['NBA']
        if request.form['submit'] == 'Search':
            search = request.form['search']
            for article in NBA.find():
                if article['Title'] == search:
                    articles.append(article)
        else:
            for article in NBA.find():
                articles.append(article)
            articles = sorted(articles, key=lambda k: k['Updated'], reverse=True) 
    return render_template('news.html', articles=articles, num_instances=len(articles), filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")
    
@app.route('/Year', methods=['GET', 'POST'])
def Year():
    # db_year = client['Years']
    # collection_year = db_year['NBA']
    # year_info_documents = []
    # for document in collection_year.find():
    #     year_info_documents.append(document)
    # year_info_documents = sorted(year_info_documents, key=lambda k: k['Year'],reverse=True)

    year1 = {
        "Year": "1947",
        "Western Champion": "Golden State Warriors",
        "Eastern Champion": "Chicago Stags",
        "NBA Finals Winner": "Golden State Warriors",
        "Season MVP": "",
        "Finals MVP": ""
    }

    year2 = {
        "Year": "1949",
        "Western Champion": "Los Angeles Lakers",
        "Eastern Champion": "Washington Capitols",
        "NBA Finals Winner": "Los Angeles Lakers",
        "Season MVP": "",
        "Finals MVP": ""
    }

    year3 = {
        "Year": "1950",
        "Western Champion": "Los Angeles Lakers",
        "Eastern Champion": "Syracuse Nationals (76ers)",
        "NBA Finals Winner": "Los Angeles Lakers",
        "Season MVP": "",
        "Finals MVP": ""
    }

    year_info_documents = []
    year_info_documents.append(year1)
    year_info_documents.append(year2)
    year_info_documents.append(year3)


    return render_template('year.html',year_info_documents=year_info_documents)

@app.route('/Franchise_Leaders')
def record():
    # db_franLeaders = client['Franchise_Leaders']
    # collection_franLeaders = db_franLeaders['NBA']
    # franLeaders_documents = []
    # for document in collection_franLeaders.find():
    #     franLeaders_documents.append(document)
    # franLeaders_documents = sorted(franLeaders_documents,key=lambda k: k['Team Name'])

    record1 = {
        "Team Name": "Atlanta Hawks",
        "PTS Franchise Leader Name": "Dominique Wilkins",
        "Total Points": "23292",
        "AST Franchise Leader Name": "Doc Rivers",
        "Total Assists": "3866",
        "REB Franchise Leader Name": "Bob Pettit",
        "Total Rebounds": "12849",
        "BLK Franchise Leader Name": "Tree Rollins",
        "Total Blocks": "2283",
        "STL Franchise Leader Name": "Mookie Blaylock",
        "Total Steals": "1321"
    }

    record2 = {
        "Team Name": "Boston Celtics",
        "PTS Franchise Leader Name": "John Havlicek",
        "Total Points": "26395",
        "AST Franchise Leader Name": "Bob Cousy",
        "Total Assists": "6945",
        "REB Franchise Leader Name": "Bill Russell",
        "Total Rebounds": "21620",
        "BLK Franchise Leader Name": "Robert Parish",
        "Total Blocks": "1703",
        "STL Franchise Leader Name": "Paul Pierce",
        "Total Steals": "1583"
    }

    record3 = {
        "Team Name": "Cleveland Cavaliers",
        "PTS Franchise Leader Name": "Lebron James",
        "Total Points": "23119",
        "AST Franchise Leader Name": "Lebron James",
        "Total Assists": "6228",
        "REB Franchise Leader Name": "Lebron James",
        "Total Rebounds": "6190",
        "BLK Franchise Leader Name": "Zydrunas Ilgauskas",
        "Total Blocks": "1269",
        "STL Franchise Leader Name": "Lebron James",
        "Total Steals": "1376"
    }

    franLeaders_documents = []
    franLeaders_documents.append(record1)
    franLeaders_documents.append(record2)
    franLeaders_documents.append(record3)

    
    return render_template('franchiseleaders.html',franLeaders_documents=franLeaders_documents)

@app.route('/Fantasy', methods=['GET', 'POST'])
def Fantasy():

    player1 = {
        "Name": "Ray Allen",
        "PTS": "18.9",
        "AST": "3.4",
        "REB": "4.1"
    }

    player2 = {
        "Name": "Larry Bird",
        "PTS": "24.3",
        "AST": "6.3",
        "REB": "10"
    }

    player3 = {
        "Name": "Dave Cowens",
        "PTS": "17.6",
        "AST": "3.8",
        "REB": "13.6"
    }

    player4 = {
        "Name": "Andrew Drummond",
        "PTS": "17.7",
        "AST": "2.7",
        "REB": "15.2"
    }

    player5 = {
        "Name": "Reggie Miller",
        "PTS": "18.2",
        "AST": "3",
        "REB": "3"
    }



    # players_db = client['Players']
    # NBA = players_db['NBA_selected']
    all_players = []
    all_players.append(player1)
    all_players.append(player2)
    all_players.append(player3)
    all_players.append(player4)
    all_players.append(player5)

    # for player in NBA.find():
    #     all_players.append(player)
    if request.method == 'POST':
        selected_players_names = request.form.getlist("player")
        if len(selected_players_names) == 0:
            return render_template('fantasy.html',all_players=all_players, team_formed = False, selected_players=[])
        elif len(selected_players_names) > 5:
            selected_players_names = selected_players_names[:5]

        selected_players = []
        average_PTS = 0
        average_AST = 0
        average_REB = 0
        for player in all_players:
            if player['Name'] in selected_players_names:
                selected_players.append(player)
                average_PTS += (float)(player['PTS'])
                average_AST += (float)(player['AST'])
                average_REB += (float)(player['REB'])
        average_PTS /= len(selected_players) 
        average_AST /= len(selected_players)
        average_REB /= len(selected_players)

        average_PTS = round(average_PTS, 1)
        average_AST = round(average_AST, 1)
        average_REB = round(average_REB, 1)
        return render_template('fantasy.html',all_players=all_players, team_formed=True, selected_players=selected_players, average_PTS=average_PTS, average_AST=average_AST, average_REB=average_REB)
    else:
        return render_template('fantasy.html',all_players=all_players, team_formed = False, selected_players=[])


@app.route('/Coaches',methods = ['GET','POST'])

def coaches():

    

    coach1 = {
        "Team Name": "Atlanta Hawks",
        "Coach Name": "Lloyd Pierce",
        "Coach Type": "Head Coach",
        "Season": "2019-2020"
    }

    coach2 = {
        "Team Name": "Boston Celtics",
        "Coach Name": "Brad Stevens",
        "Coach Type": "Head Coach",
        "Season": "2019-2020"
    }

    coach3 = {
        "Team Name": "Cleveland Cavaliers",
        "Coach Name": "JB Bickerstaff",
        "Coach Type": "Head Coach",
        "Season": "2019-2020"
    }

    coaches_documents = []
    coaches_documents.append(coach1)
    coaches_documents.append(coach2)
    coaches_documents.append(coach3)

    if request.method == "POST":
        coach_requested = request.form['coach_choices']
        
        #     coach_info = collection_coaches.find_one({"Coach Name": coach_requested})

        if coach_requested == "Lloyd Pierce":
            team_name = "Atlanta Hawks"
            coach_name = coach_requested
            coach_type = "Head Coach"
            season_type = "2019-2020"
        elif coach_requested == "Brad Stevens":
            team_name = "Boston Celtics"
            coach_name = coach_requested
            coach_type = "Head Coach"
            season_type = "2019-2020"
        elif coach_requested == "JB Bickerstaff":
            team_name = "Cleveland Cavaliers"
            coach_name = coach_requested
            coach_type = "Head Coach"
            season_type = "2019-2020"

        # team_name = coach_info['Team Name']
        # coach_name = coach_requested
        # coach_type = coach_info['Coach Type']
        # season_type = coach_info['Season']

        return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=True,team_name=team_name,coach_name=coach_name,coach_type=coach_type,season_type=season_type)


    else:

        return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=False)

    # db_coaches = client['Coaches']
    # collection_coaches = db_coaches['NBA']
    # coaches_documents = []
    # for document in collection_coaches.find():
    #     coaches_documents.append(document)
    # if request.method == "POST":

    #     coach_requested = request.form['coach_choices']
    #     if coach_requested == "":
    #         return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=False)
 
    #     coach_info = collection_coaches.find_one({"Coach Name": coach_requested})

    #     team_name = coach_info['Team Name']
    #     coach_name = coach_requested
    #     coach_type = coach_info['Coach Type']
    #     season_type = coach_info['Season']

    #     return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=True,team_name=team_name,coach_name=coach_name,coach_type=coach_type,season_type=season_type)
    # else:
    #     return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=False)
    

    





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
    teamList = teams.get_teams()
    if request.method == 'POST':
        person = request.form['playerchoices']
        if person == "":
            return render_template('favplayer.html', playerList = playerList, teamList=teamList)

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


        return render_template('favplayer.html', teamList=teamList, playerList = playerList, addPlayer = addPlayer, name=name, active=active, yearsActive= yearsActive, teamName=teamName, teamCity=teamCity, jersey = jersey, position=position, height=height, weight=weight, draftYear=draftYear, draftRound=draftRound, draftNumber=draftNumber, birth=birth, school=school, PTS=PTS, AST=AST, REB=REB)
    else:
        return render_template('favplayer.html', teamList=teamList, playerList = playerList)





@app.route('/comparison')

def comparison():
    playerList = players.get_players()
    teamList = teams.get_teams()
    if request.method == 'POST':
        return render_template('comparison.html', playerList=playerList, teamList=teamList)

    else:

        return render_template('comparison.html', playerList=playerList, teamList=teamList)





@app.route('/account')

def account():

    return render_template('login.html')





@app.route('/pop-up')

def popup():

    pass


# teams instances, temporary#
@app.route('/sixers')
def team1():
    return render_template('team1.html')

@app.route('/aces')
def team2():
    return render_template('team2.html')

@app.route('/bucks')
def team3():
    return render_template('team3.html')
    

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)

