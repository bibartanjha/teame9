from flask import Flask, render_template, url_for, request, redirect

from nba_api.stats.static import players, teams

from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster

import pymongo

from pymongo import MongoClient





app = Flask(__name__)



client_year = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Years?retryWrites=true&w=majority")
client_trade = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
client_teams = MongoClient("mongodb+srv://Andrew:w66lPqEEXd7YZPZB@teame9db.kngdj.gcp.mongodb.net/Teams?retryWrites=true&w=majority")



@app.route('/')

def root():

    return render_template('index.html')





@app.route('/AboutPage')

def AboutPage():

    return render_template('about.html')





@app.route('/Players', methods=['GET', 'POST'])

def Players():

    all_players = []

    

    for player in players.get_players():

        all_players.append(player['full_name'])

    if request.method == 'POST':

        player_name = request.form['content']

        if player_name == "":

            return render_template('players.html', all_players=all_players)

        find_player = players.find_players_by_full_name(player_name)

        try:

            player_id = find_player[0]['id']

        except:

            return render_template('players.html', all_players=all_players)

        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)



        commoninfo_headers = player_info.common_player_info.get_dict()['headers']

        commoninfo_data = player_info.common_player_info.get_dict()['data']



        name = "NAME: " + find_player[0]['full_name']

        name = name.upper()

        team = "Team: " + commoninfo_data[0][commoninfo_headers.index('TEAM_CITY')] + " " + commoninfo_data[0][commoninfo_headers.index('TEAM_NAME')] 

        position = "Position: " + commoninfo_data[0][commoninfo_headers.index('POSITION')]

        jersey = "Jersey: " + commoninfo_data[0][commoninfo_headers.index('JERSEY')]

        height = "Height: " + commoninfo_data[0][commoninfo_headers.index('HEIGHT')]

        weight = "Weight: " + commoninfo_data[0][commoninfo_headers.index('WEIGHT')]

        draft_year = "Year: " + str(commoninfo_data[0][commoninfo_headers.index('DRAFT_YEAR')])

        draft_round = "Round: " + str(commoninfo_data[0][commoninfo_headers.index('DRAFT_ROUND')])

        draft_number = "Number: " + str(commoninfo_data[0][commoninfo_headers.index('DRAFT_NUMBER')])

        bd = "Birth Date: " + commoninfo_data[0][commoninfo_headers.index('BIRTHDATE')][:10]

        school = "School: "+ commoninfo_data[0][commoninfo_headers.index('SCHOOL')]



        years = "Years Active: " + str(commoninfo_data[0][commoninfo_headers.index('FROM_YEAR')]) + " - "

        if find_player[0]['is_active']==True:

            years += "Present"

        else:

            years += str(commoninfo_data[0][commoninfo_headers.index('TO_YEAR')])



        stats_headers = player_info.player_headline_stats.get_dict()['headers']

        stats_data = player_info.player_headline_stats.get_dict()['data']

        PTS = "PTS: " + str(stats_data[0][stats_headers.index('PTS')])

        AST = "AST: " + str(stats_data[0][stats_headers.index('AST')])

        REB = "REB: " + str(stats_data[0][stats_headers.index('REB')])



        general = "General"

        bio = "Bio"

        stats = "Stats"

        draft = "Draft"

        

        return render_template('players.html', all_players=all_players, general=general, bio=bio, stats=stats, draft=draft, name=name, team=team, position=position, jersey=jersey, years=years, bd=bd, school=school, height=height, weight=weight, draft_year=draft_year, draft_round=draft_round, draft_number=draft_number, PTS=PTS, AST=AST, REB=REB)

    else:

        return render_template('players.html', all_players=all_players)





@app.route('/Teams', methods=['GET', 'POST'])

def Teams():

    all_teams = []

    for team in teams.get_teams():

        all_teams.append(team['full_name'])

    if request.method == 'POST':

        team_name = request.form['content']

        if team_name == "":

            return render_template('teams.html', all_teams=all_teams)

        find_team = teams.find_teams_by_full_name(team_name)

        try:

            team_id = find_team[0]['id']

        except:

            return render_template('teams.html', all_teams=all_teams)

        team_info = teaminfocommon.TeamInfoCommon(team_id=team_id)



        commoninfo_headers = team_info.team_info_common.get_dict()['headers']

        commoninfo_data = team_info.team_info_common.get_dict()['data']

        name = "TEAM: " + find_team[0]['full_name']     

        name = name.upper()

        city = "Location: " + find_team[0]['city'] + ", " + find_team[0]['state']  

        conference = "Conference: " + commoninfo_data[0][commoninfo_headers.index('TEAM_CONFERENCE')]

        division = "Divison: " + commoninfo_data[0][commoninfo_headers.index('TEAM_DIVISION')]

        season_year = "Season-Year: " + str(commoninfo_data[0][commoninfo_headers.index('SEASON_YEAR')])

        W = "Wins: " + str(commoninfo_data[0][commoninfo_headers.index('W')])

        L = "Losses: " + str(commoninfo_data[0][commoninfo_headers.index('L')])

        PCT = "PCT: " + str(commoninfo_data[0][commoninfo_headers.index('PCT')])

        conf_rank = "Conference Rank: " + str(commoninfo_data[0][commoninfo_headers.index('CONF_RANK')])

        div_rank = "Division Rank: " + str(commoninfo_data[0][commoninfo_headers.index('DIV_RANK')])

        years = "Years: " + str(find_team[0]['year_founded']) + " - " 

        end_year = str(commoninfo_data[0][commoninfo_headers.index('MAX_YEAR')])

        if end_year == "2019" or end_year == "2020":

            years += "Present"

        else:

            years += end_year

        

        team_details = teamdetails.TeamDetails(team_id=team_id)

        

        background_headers = team_details.team_background.get_dict()['headers']

        background_data = team_details.team_background.get_dict()['data']

        arena = "Arena: " + background_data[0][background_headers.index('ARENA')]

        owner = "Owner: " + background_data[0][background_headers.index('OWNER')]

        coach = "Coach: " + background_data[0][background_headers.index('HEADCOACH')]



        champion_headers = team_details.team_awards_championships.get_dict()['headers']

        champion_data = team_details.team_awards_championships.get_dict()['data']

        championships_list = []

        for entry in champion_data:

            championships_list.append(str(entry[0]) + " against " + entry[1])





        team_roster = commonteamroster.CommonTeamRoster(team_id=team_id, season="2019-20")

        roster_headers = team_roster.common_team_roster.get_dict()['headers']

        roster_data = team_roster.common_team_roster.get_dict()['data']

        roster_list = []

        for player in roster_data:

            roster_list.append(player[roster_headers.index('PLAYER')] + " (Position: " + player[roster_headers.index('POSITION')] + ")")



        general = "General"

        championships = "Championships"

        roster = "Roster"



        return render_template('teams.html', all_teams=all_teams, general=general, championships=championships, roster=roster, name=name, city=city, conference=conference, division=division, season_year=season_year, W=W, L=L, PCT=PCT, conf_rank=conf_rank, div_rank=div_rank, years=years, arena=arena, owner=owner, coach=coach, championships_list=championships_list, roster_list=roster_list)

    else:

        return render_template('teams.html', all_teams=all_teams)



@app.route('/News', methods=['GET', 'POST'])

def News():

    if request.method == 'POST':

        pass

    else:

        return render_template('news.html')





@app.route('/Year', methods=['GET', 'POST'])

def Year():

    if request.method == 'POST':

        year_requested = request.form['content']

        if year_requested == "":

            return render_template('year.html')

        db_year = client_year.Years

        collection_year = db_year["NBA"]

        document_year = collection_year.find_one({"Year": year_requested})

        finalsWinnerName = "NBA Finals Chamption: " + document_year['NBA Finals Winner']

        westWinnerName = "Western Conference Champion: " + document_year['Western Champion']

        eastWinnerName = "Eastern Conference Champion: " + document_year['Eastern Champion']

        finalsMVPName = "Finals MVP: " + document_year['Finals MVP']

        seasonMVPName = "Season MVP: " + document_year['Season MVP']

        return render_template('year.html', finalsWinnerName=finalsWinnerName,westWinnerName=westWinnerName,eastWinnerName=eastWinnerName,finalsMVPName=finalsMVPName,seasonMVPName=seasonMVPName)

    else:

        return render_template('year.html')







@app.route('/Records')

def record():

    return render_template('records.html')

    #find team with most championships
    # db_teams = client_teams.Teams
    # collection_teams = db_teams['NBA']

    # team_name = ""
    # titles = 0
    # for i in collection_teams:
    #     number_of_championships = len(i['Championships'])
    #     if titles <= number_of_championships:
    #         titles = number_of_championships
    #         team_name = i['Name']

    # team_championship_str = team_name + " holds the record with " + str(titles) + " championships"

    # return render_template('records.html',record_team_championships=team_championship_str)





@app.route('/TradeSim',methods = ['GET','POST'])

def TradeSim():

    if request.method == 'POST':

        player1 = request.form['playerName1']
        player2 = request.form['playerName2']

        if player1 == "" or player2 == "":

            return render_template('tradeSim.html')

        db_trade = client_trade.Players
        collection_trade = db_trade['NBA_selected']
        player1_info = collection_trade.find_one({"Name": player1})
        player2_info = collection_trade.find_one({"Name": player2})

        player1_stats = float(player1_info['PTS'])
        player2_stats = float(player2_info['PTS'])

        valid_trade = ""

        if abs(player1_stats - player2_stats) > 5:
            valid_trade = "Invalid trade between " + player1_info['Name'] + " and " + player2_info['Name']
        else:
            valid_trade = "Valid trade between " + player1_info['Name'] + " and " + player2_info['Name']

        return render_template('tradeSim.html',valid_trade = valid_trade)

    else:
        return render_template('tradeSim.html')





@app.route('/Settings')

def Settings():

    return render_template('settings.html')





@app.route('/favteam')

def favteam():

    if request.method == 'POST':

        pass

    else:

        return render_template('favteam.html')





@app.route('/favplayer')

def favplayer():

    if request.method == 'POST':

        pass

    else:

        return render_template('favplayer.html')





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

