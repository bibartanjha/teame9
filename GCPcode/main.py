from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/AboutPage')
def AboutPage():
    pass


@app.route('/Players')
def Players():
    pass


@app.route('/Teams')
def Teams():
    pass


@app.route('/News')
def News():
    pass


@app.route('/Year')
def Year():
    return render_template('year.html')


@app.route('/PlayoffSim')
def PlayoffSim():
    return render_template('playoffSim.html')


@app.route('/TradeSim')
def TradeSim():
    return render_template('tradeSim.html')


@app.route('/Settings')
def Settings():
    pass


@app.route('/favteam')
def favteam():
    pass


@app.route('/favplayer')
def favplayer():
    pass


@app.route('/comparison')
def comparison():
    pass


@app.route('/account')
def account():
    pass


@app.route('/pop-up')
def popup():
    pass


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
