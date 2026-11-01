from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@me_2006",
    database="tourismrecom_db"
)

cursor = db.cursor(dictionary=True)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')


# Recommendation Route
@app.route('/recommend', methods=['POST'])
def recommend():

    budget = int(request.form['budget'])
    category = request.form['category']
    days = int(request.form['days'])

    query = """
    SELECT * FROM destinations
    WHERE category = %s
    AND budget <= %s
    AND days <= %s
    """

    values = (category, budget, days)

    cursor.execute(query, values)

    results = cursor.fetchall()

    recommendations = []

    for place in results:

        score = 0

        if place['category'] == category:
            score += 50

        if place['budget'] <= budget:
            score += 30

        if place['days'] <= days:
            score += 20

        place['score'] = score
        recommendations.append(place)

    return render_template(
        'results.html',
        places=recommendations
    )


if __name__ == '__main__':
    app.run(debug=True)