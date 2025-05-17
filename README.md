# Ad Campaign Performance Tracker

A web application to track and visualize ad campaign metrics, built for my Google Web Solutions Engineer portfolio.

## Features
- Add campaign data (name, date, clicks, impressions, conversions) via a form.
- View data in a table with calculated conversion rates.
- Edit existing campaigns to update details.
- Delete campaigns from the database.
- Visualize clicks and conversions in a bar chart.
- Built with Flask, MySQL, Pandas, and Matplotlib.

## Setup
1. Clone the repository: `git clone https://github.com/anandhupl/ad-campaign-tracker.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MySQL database with `schema.sql`:
   - Run: `mysql -u root -p < schema.sql`
4. Run the app: `python app.py`
5. Access at `http://127.0.0.1:5000`

## Technologies
- Flask: Web framework
- MySQL: Database
- Pandas/Matplotlib: Data analysis and visualization
- HTML/CSS: Frontend
- Python 3.11: Backend

## Notes
- Resolved MySQL issues (ERROR 1045, ERROR 2003, ibdata1 permissions, SQL syntax errors) by configuring `my.ini`, granting permissions, resetting the root password, and fixing SQL commands.
- Fixed `pandas` installation by switching to 64-bit Python 3.11 and using Visual Studio Build Tools.
- Handled `TemplateNotFound` error by ensuring correct template files (`index.html`, `view.html`, `edit.html`, `chart.html`).
- Implemented full CRUD functionality (Create, Read, Update, Delete) for campaigns like "Spring Sale" and "Summer Sale 2025 Final."
- Error handling ensures valid input (non-negative numbers).

- ## Screenshot
![App Screenshot](https://github.com/user-attachments/assets/864cdb09-f1a5-4f45-8b62-4fb294963cd0)
