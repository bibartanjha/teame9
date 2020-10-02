
function simulateTrade() {
  var x = document.getElementById("playerName1").value;
  var y = document.getElementById("playerName2").value;
//   document.getElementById("poop").innerHTML = x;
//   document.getElementById("head").innerHTML = y;
}



function simSeason(){

    var nbaTeamNames = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets",
                "Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers",
                "Dallas Mavericks","Denver Nuggets","Detroit Pistons",
                "Golden State Warriors","Houston Rockets","Indiana Pacers",
                "Los Angeles Clippers","Los Angeles Lakers","Memphis Grizzlies",
                "Miami Heat","Milwaukee Bucks","Minnesota Timberwolves",
                "New Orleans Pelicans","New York Knicks","Oklahoma City Thunder",
                "Orlando Magic","Philadelphia 76ers","Phoenix Suns",
                "Portland Trail Blazers","Sacramento Kings","San Antonio Spurs",
                "Toronto Raptors","Utah Jazz","Washington Wizards"];

    var playoffTeams = findPlayoffTeams(nbaTeamNames);

    document.getElementById("playoffTeam1").innerHTML = playoffTeams[0] + " #1 seed"
    document.getElementById("playoffTeam2").innerHTML = playoffTeams[1] + " #2 seed"
    document.getElementById("playoffTeam3").innerHTML = playoffTeams[2] + " #3 seed"
    document.getElementById("playoffTeam4").innerHTML = playoffTeams[3] + " #4 seed"
    document.getElementById("playoffTeam5").innerHTML = playoffTeams[4] + " #5 seed"
    document.getElementById("playoffTeam6").innerHTML = playoffTeams[5] + " #6 seed"
    document.getElementById("playoffTeam7").innerHTML = playoffTeams[6] + " #7 seed"
    document.getElementById("playoffTeam8").innerHTML = playoffTeams[7] + " #8 seed"

}

function findPlayoffTeams(nbaTeamNames){

    var playoffTeams = [];
    var i;
    for(i = 0; i < 8; i++){

        var team = nbaTeamNames[(Math.floor((Math.random() * 29) + 1))];
        if(i == 0){
            playoffTeams.push(team);
        }
        else {
            if(playoffTeams.indexOf(team) > -1){
                i--;
            }
            else {
                playoffTeams.push(team);
            }
        }

    }

    return playoffTeams;

}

function displayNews(){

    var year = document.getElementById("year").value;
    document.getElementById("yearDisplay").innerHTML = year;
}
