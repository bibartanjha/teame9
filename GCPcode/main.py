from flask import Flask, render_template, url_for, request, redirect

import nba_api

from nba_api.stats.static import players, teams

from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster

import pymongo

from pymongo import MongoClient
from django.core.paginator import Paginator
import csv
'''
import numpy as np

import requests

import time

import http.client

import json

import random
'''

#chase username and password accordingly

# try:
#client = pymongo.MongoClient("mongodb+srv://Bibartan:bibpass@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
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
    players = []
    csv_file = csv.reader(open('nba_players.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        players.append(dict_1)
    players = sorted(players, key=lambda k: k['Name'])
    
    if request.method == 'GET':
        which_button = request.args.get('submit')
        if which_button == "Search" or which_button == "Default":
            if which_button == "Search":
                search = request.args.get('search')
                players_2 = []
                for player in players:
                    if (player['Name'] == search):
                        players_2.append(player)
                players = players_2
            p = Paginator(players, 9) #9 entries per page
            num_pages = p.num_pages
            page = request.args.get('page', 1, type=int)
            posts = p.get_page(page).object_list
            return render_template('players.html', page=page, posts=posts, num_pages=num_pages, players=players, num_instances=len(players), filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')

        filter_status = request.args.get('Status')
        if not (filter_status == None or filter_status == "None" or filter_status == "All statuses"):
            players_with_status = []
            for player in players:
                if player['Status'] == filter_status:
                    players_with_status.append(player)
            players=players_with_status

        filter_position = request.args.get('Position')
        if not (filter_position == None or filter_position == "None" or filter_position == "All positions"):
            players_in_position = []
            for player in players:
                if player['Position'] == filter_position:
                    players_in_position.append(player)
            players=players_in_position

        filter_team = request.args.get('Team')
        if not (filter_team == None or filter_team == "None" or filter_team == "All teams"):
            players_in_team = []
            for player in players:
                if player['Team'] == filter_team:
                    players_in_team.append(player)
            players=players_in_team


        sort = request.args.get('Sort')
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


        p = Paginator(players, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('players.html', page=page, posts=posts, num_pages=num_pages, players=players, num_instances=len(players), filter_status=filter_status, filter_position=filter_position, filter_team=filter_team, sort=sort)
    else: 
        p = Paginator(players, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('players.html', page=page, posts=posts, num_pages=num_pages, players=players, num_instances=len(players), filter_status="All statuses", filter_position="All positions", filter_team="All teams", sort='Default: Name (A-Z)')


@app.route('/Teams', methods=['GET', 'POST'])
def Teams():
    teams = []
    csv_file = csv.reader(open('nba_teams.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        teams.append(dict_1)

    csv_file = csv.reader(open('wnba_teams.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        teams.append(dict_1)
    
    teams = sorted(teams, key=lambda k: k['Name'])

    if request.method == 'GET':
        which_button = request.args.get('submit')
        if which_button == "Search" or which_button == "Default":
            if which_button == "Search":
                search = request.args.get('search')
                teams_2 = []
                for team in teams:
                    if (team['Name'] == search):
                        teams_2.append(team)
                teams = teams_2
            p = Paginator(teams, 9) #9 entries per page
            num_pages = p.num_pages
            page = request.args.get('page', 1, type=int)
            posts = p.get_page(page).object_list
            return render_template('teams.html', page=page, posts=posts, num_pages=num_pages, teams=teams, num_instances=len(teams), filter_league="All leagues", filter_conference="All conferences", filter_division="All divisions", sort='Default: Team Name (A-Z)')

        filter_league = request.args.get('League')
        if not (filter_league == None or filter_league == "None" or filter_league == "All leagues"):
            teams_in_league = []
            for team in teams:
                if team['League'] == filter_league:
                    teams_in_league.append(team)
            teams=teams_in_league

        filter_conference = request.args.get('Conference')
        if not (filter_conference == None or filter_conference == "None" or filter_conference == "All conferences"):
            league = filter_conference.split(" ")[0]
            conference = filter_conference.split(" ")[1]
            teams_in_conference = []
            for team in teams:
                if team['League'] == league and team['Conference'] == conference:
                    teams_in_conference.append(team)
            teams=teams_in_conference

        filter_division = request.args.get('Division')
        if not (filter_division == None or filter_division == "None" or filter_division == "All divisions"):
            teams_in_division = []
            for team in teams:
                if team['League'] == 'NBA':
                    if team['Division'] == filter_division:
                        teams_in_division.append(team)
            teams=teams_in_division


        sort = request.args.get('Sort') 
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
        p = Paginator(teams, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('teams.html', page=page, posts=posts, num_pages=num_pages, teams=teams, num_instances=len(teams), filter_league=filter_league, filter_conference=filter_conference, filter_division=filter_division, sort=sort)
    else:
        p = Paginator(teams, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('teams.html', page=page, posts=posts, num_pages=num_pages, teams=teams, num_instances=len(teams), filter_league="All leagues", filter_conference="All conferences", filter_division="All divisions", sort='Default: Team Name (A-Z)')

@app.route('/News', methods=['GET', 'POST'])
def News():
    articles = []
    csv_file = csv.reader(open('news.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        articles.append(dict_1)
    articles = sorted(articles, key=lambda k: k['Updated'], reverse=True)

    if request.method == 'GET':
        which_button = request.args.get('submit')
        if which_button == "Search" or which_button == "Default":
            if which_button == "Search":
                search = request.args.get('search')
                articles_2 = []
                for art in articles:
                    if (art['Updated'][:10] == search):
                        articles_2.append(art)
                articles = articles_2
            p = Paginator(articles, 9) #9 entries per page
            num_pages = p.num_pages
            page = request.args.get('page', 1, type=int)
            posts = p.get_page(page).object_list
            return render_template('news.html', page=page, posts=posts, num_pages=num_pages, articles=articles, num_instances=len(articles), filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")

        filter_category = request.args.get('Category')
        if not (filter_category == None or filter_category == "None" or filter_category == "All categories"):
            articles_in_category = []
            for article in articles:
                if article['Categories'] == filter_category:
                    articles_in_category.append(article)
            articles=articles_in_category

        filter_team = request.args.get('Team')
        if not (filter_team == None or filter_team == "None" or filter_team == "All teams"):
            articles_for_team = []
            for article in articles:
                if article['Team'] == filter_team:
                    articles_for_team.append(article)
            articles=articles_for_team

        sort = request.args.get('Sort')
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

        p = Paginator(articles, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('news.html', page=page, posts=posts, num_pages=num_pages, articles=articles, num_instances=len(articles), filter_category=filter_category, filter_team=filter_team, sort=sort)
    else:
        p = Paginator(articles, 9) #9 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('news.html', page=page, posts=posts, num_pages=num_pages, articles=articles, num_instances=len(articles), filter_category="All categories", filter_team="All teams", sort="Default: Date (Latest to Earliest)")
    
@app.route('/newsInstance1', methods=['GET', 'POST'])
def newsInstance_one():
    
    return render_template('news1.html')

@app.route('/newsInstance2', methods=['GET', 'POST'])
def newsInstance_two():
    
    return render_template('news2.html')

@app.route('/newsInstance3', methods=['GET', 'POST'])
def newsInstance_three():
    
    return render_template('news3.html')

@app.route('/Year', methods=['GET', 'POST'])
def Year():
    # db_year = client['Years']
    # collection_year = db_year['NBA']
    # year_info_documents = []
    # for document in collection_year.find():
    #     year_info_documents.append(document)
    # year_info_documents = sorted(year_info_documents, key=lambda k: k['Year'],reverse=True)

    year_info_documents = []
    csv_file = csv.reader(open('years.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        year_info_documents.append(dict_1)
    year_info_documents = sorted(year_info_documents, key=lambda k: k['Year'], reverse=True)

    '''
    year_info_documents = []
    year_info_documents.append(year1)
    year_info_documents.append(year2)
    year_info_documents.append(year3)

    '''
    return render_template('year.html',year_info_documents=year_info_documents)

@app.route('/Franchise_Leaders')
def record():
    # db_franLeaders = client['Franchise_Leaders']
    # collection_franLeaders = db_franLeaders['NBA']
    # franLeaders_documents = []
    # for document in collection_franLeaders.find():
    #     franLeaders_documents.append(document)
    # franLeaders_documents = sorted(franLeaders_documents,key=lambda k: k['Team Name'])

    franLeaders_documents = []
    csv_file = csv.reader(open('franchise_leaders.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        franLeaders_documents.append(dict_1)
    franLeaders_documents = sorted(franLeaders_documents, key=lambda k: k['Team Name'])

    return render_template('franchiseleaders.html',franLeaders_documents=franLeaders_documents)

@app.route('/Fantasy', methods=['GET', 'POST'])
def Fantasy():
    all_players = []
    
    csv_file = csv.reader(open('nba_players.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        all_players.append(dict_1)
    all_players = sorted(all_players, key=lambda k: k['Name'])
    
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
    coaches_documents = []

    csv_file = csv.reader(open('coaches.csv', "r"), delimiter=",")
    rows = []
    for row in csv_file:
        rows.append(row)
    headers = rows[0]

    for i in range (1, len(rows)):
        curr_row = rows[i]
        dict_1 = {};
        for j in range (len(headers)):
            dict_1[headers[j]] = curr_row[j]
        coaches_documents.append(dict_1)
    coaches_documents = sorted(coaches_documents, key=lambda k: k['Coach Name'])

    if request.method == "POST":
        coach_requested = request.form['coach_choices']
        coach_selected = coaches_documents[0]
        for coach in coaches_documents:
            if (coach['Coach Name'] == coach_requested):
                coach_selected = coach
                break
        team_name = coach_selected['Team Name']
        coach_name = coach_selected['Coach Name']
        coach_type = coach_selected['Coach Type']
        season_type = coach_selected['Season']


        '''    coach_info = collection_coaches.find_one({"Coach Name": coach_requested})

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
        '''

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

