from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': 'A7736604688U',
    'host': 'localhost',
    'database': 'ad_tracker',
    'port': 3306
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            campaign_name = request.form['campaign_name']
            date = request.form['date']
            clicks = int(request.form['clicks'])
            impressions = int(request.form['impressions'])
            conversions = int(request.form['conversions'])
            if clicks < 0 or impressions < 0 or conversions < 0:
                raise ValueError("Values cannot be negative")
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO campaigns (campaign_name, date, clicks, impressions, conversions) VALUES (%s, %s, %s, %s, %s)",
                           (campaign_name, date, clicks, impressions, conversions))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view'))
        except (ValueError, mysql.connector.Error) as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html', error=None)

@app.route('/view')
def view():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT *, (conversions / NULLIF(clicks, 0) * 100) AS conversion_rate FROM campaigns")
    campaigns = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view.html', campaigns=campaigns)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        try:
            campaign_name = request.form['campaign_name']
            date = request.form['date']
            clicks = int(request.form['clicks'])
            impressions = int(request.form['impressions'])
            conversions = int(request.form['conversions'])
            if clicks < 0 or impressions < 0 or conversions < 0:
                raise ValueError("Values cannot be negative")
            cursor.execute("UPDATE campaigns SET campaign_name=%s, date=%s, clicks=%s, impressions=%s, conversions=%s WHERE id=%s",
                           (campaign_name, date, clicks, impressions, conversions, id))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('view'))
        except (ValueError, mysql.connector.Error) as e:
            cursor.execute("SELECT * FROM campaigns WHERE id=%s", (id,))
            campaign = cursor.fetchone()
            cursor.close()
            conn.close()
            return render_template('edit.html', campaign=campaign, error=str(e))
    cursor.execute("SELECT * FROM campaigns WHERE id=%s", (id,))
    campaign = cursor.fetchone()
    cursor.close()
    conn.close()
    if campaign:
        return render_template('edit.html', campaign=campaign, error=None)
    return redirect(url_for('view'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM campaigns WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Error deleting campaign: {e}")
    return redirect(url_for('view'))

@app.route('/chart')
def chart():
    conn = get_db_connection()
    df = pd.read_sql("SELECT campaign_name, clicks, conversions FROM campaigns", conn)
    conn.close()
    plt.figure(figsize=(10, 5))
    plt.bar(df['campaign_name'], df['clicks'], label='Clicks')
    plt.bar(df['campaign_name'], df['conversions'], label='Conversions', alpha=0.5)
    plt.xlabel('Campaign')
    plt.ylabel('Count')
    plt.title('Clicks and Conversions by Campaign')
    plt.legend()
    chart_path = os.path.join('static', 'chart.png')
    plt.savefig(chart_path)
    plt.close()
    return render_template('chart.html', chart_url='static/chart.png')

if __name__ == '__main__':
    app.run(debug=True)