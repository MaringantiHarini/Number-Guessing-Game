from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key

MAX_ATTEMPTS = 7

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = MAX_ATTEMPTS
        session['game_over'] = False

    message = ''
    status = ''
    game_over = session.get('game_over', False)
    attempts_left = session.get('attempts', MAX_ATTEMPTS)

    if request.method == 'POST' and not game_over:
        try:
            guess = int(request.form['guess'])
            number = session['number']
            session['attempts'] -= 1
            attempts_left = session['attempts']

            if guess == number:
                message = f"🎉 Correct! The number was {number}."
                status = 'success'
                session['game_over'] = True
            elif session['attempts'] == 0:
                message = f"💥 Out of attempts! The number was {number}."
                status = 'error'
                session['game_over'] = True
            elif guess < number:
                message = "📉 Too low!"
                status = 'error'
            else:
                message = "📈 Too high!"
                status = 'error'
        except ValueError:
            message = "⚠️ Please enter a valid number."
            status = 'error'

    return render_template('index.html',
                           message=message,
                           status=status,
                           game_over=session.get('game_over', False),
                           attempts_left=attempts_left)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('number', None)
    session.pop('attempts', None)
    session.pop('game_over', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
