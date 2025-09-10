# Stylish Portfolio (Flask + Tailwind + JS + MySQL)

A modern, dark‑mode enabled personal portfolio built with Flask, Tailwind CSS, JavaScript, and SQLAlchemy (MySQL via PyMySQL). Includes animated neon background, projects grid, and contact form persisting messages to the database.

## Quickstart (Windows, cmd)

1. Create and activate a virtual environment
```
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Configure database
- Default fallback is SQLite at `portfolio.db` (no setup required).
- To use MySQL, set an environment variable like:
```
set SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost:3306/portfolio
```
Create the database `portfolio` in MySQL first.

4. Run the app
```
python app.py
```
Visit `http://localhost:5000`.

## Customization
- Update name/brand in `templates/base.html` and hero section in `templates/index.html`.
- Add/edit projects in the database or adjust the seed data in `app.py`.

## Production notes
- Set `SECRET_KEY` env var.
- Use a production server (e.g., `gunicorn` on Linux) and a managed MySQL. 