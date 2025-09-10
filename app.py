from datetime import datetime
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


def create_app() -> Flask:
	load_dotenv()
	app = Flask(__name__)
	app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")

	# Database configuration: prefer MySQL via env var, fallback to SQLite for local quickstart
	default_sqlite_uri = "sqlite:///portfolio.db"
	database_uri = os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI") or default_sqlite_uri
	app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db = SQLAlchemy(app)


	class Project(db.Model):
		__tablename__ = "projects"
		id = db.Column(db.Integer, primary_key=True)
		title = db.Column(db.String(200), nullable=False)
		description = db.Column(db.Text, nullable=False)
		tech_stack = db.Column(db.String(300), nullable=True)
		image_url = db.Column(db.String(500), nullable=True)
		project_url = db.Column(db.String(500), nullable=True)
		github_url = db.Column(db.String(500), nullable=True)
		created_at = db.Column(db.DateTime, default=datetime.utcnow)

		def __repr__(self) -> str:  # pragma: no cover
			return f"<Project {self.title}>"

	class Message(db.Model):
		__tablename__ = "messages"
		id = db.Column(db.Integer, primary_key=True)
		name = db.Column(db.String(200), nullable=False)
		email = db.Column(db.String(200), nullable=False)
		message = db.Column(db.Text, nullable=False)
		created_at = db.Column(db.DateTime, default=datetime.utcnow)

		def __repr__(self) -> str:  # pragma: no cover
			return f"<Message from {self.email}>"

	def init_db() -> None:
		# Create tables if they don't exist
		db.create_all()
		# Ensure portfolio projects exist/are updated with local images and GitHub links
		portfolio_projects = [
			{
				"title": "Connectify",
				"description": "A modern social platform prototype with real‑time interactions.",
				"tech_stack": "Flask, JS, Tailwind, Socket.io",
				"image_url": "images/Connectify.png",
				"project_url": "https://github.com/Rashik8606/Connectify",
				"github_url": "https://github.com/Rashik8606/Connectify",
			},
			{
				"title": "OnlineMov",
				"description": "Movie discovery app with search, filters, and watchlists.",
				"tech_stack": "Flask, TMDB API, Tailwind, SQLite",
				"image_url": "images/OnlineMov.png",
				"project_url": "https://github.com/Rashik8606/Express-basics",
				"github_url": "https://github.com/Rashik8606/Express-basics",
			},
			{
				"title": "Taskizo",
				"description": "Task management app with drag‑and‑drop and reminders.",
				"tech_stack": "Flask, JS, Tailwind, SQLAlchemy",
				"image_url": "images/Taskizo.png",
				"project_url": "https://github.com/Rashik8606/Job-Indeed",
				"github_url": "https://github.com/Rashik8606/Job-Indeed",
			},
			{
				"title": "Vegstore",
				"description": "E‑commerce demo focused on fresh produce with cart and checkout.",
				"tech_stack": "Flask, Tailwind, SQLAlchemy",
				"image_url": "images/Vegstore.png",
				"project_url": "https://github.com/Rashik8606/vegstore",
				"github_url": "https://github.com/Rashik8606/vegstore",
			},
		]
		for data in portfolio_projects:
			existing = Project.query.filter_by(title=data["title"]).first()
			if existing:
				# Replace placeholders or blanks with real data
				if not existing.description:
					existing.description = data["description"]
				if not existing.tech_stack:
					existing.tech_stack = data["tech_stack"]
				# If existing image was an external placeholder, switch to local
				if (not existing.image_url) or existing.image_url == "#" or existing.image_url.startswith("http"):
					existing.image_url = data["image_url"]
				# Always enforce correct repo links
				existing.project_url = data["project_url"]
				existing.github_url = data["github_url"]
			else:
				new_project = Project(
					title=data["title"],
					description=data["description"],
					tech_stack=data["tech_stack"],
					image_url=data["image_url"],
					project_url=data["project_url"],
					github_url=data["github_url"],
				)
				db.session.add(new_project)
		# Commit any changes
		db.session.commit()

	@app.context_processor
	def inject_now():
		return {"current_year": datetime.utcnow().year}

	# Initialize DB immediately on startup
	with app.app_context():
		init_db()

	@app.route("/")
	def home():
		projects = Project.query.order_by(Project.created_at.desc()).all()
		return render_template("index.html", projects=projects)

	@app.route("/contact", methods=["POST"])
	def contact():
		name = request.form.get("name", "").strip()
		email = request.form.get("email", "").strip()
		message_text = request.form.get("message", "").strip()

		if not name or not email or not message_text:
			flash("Please fill in all fields.", "error")
			return redirect(url_for("home"))

		try:
			msg = Message(name=name, email=email, message=message_text)
			db.session.add(msg)
			db.session.commit()
			flash("Thanks! Your message has been sent.", "success")
		except Exception as exc:  # pragma: no cover
			db.session.rollback()
			flash("Something went wrong. Please try again later.", "error")
			app.logger.exception(exc)

		return redirect(url_for("home"))

	@app.route("/admin/messages")
	def admin_messages():
		"""Admin route to view all contact messages"""
		messages = Message.query.order_by(Message.created_at.desc()).all()
		return render_template("admin_messages.html", messages=messages)

	@app.route("/api/messages")
	def api_messages():
		"""API endpoint to get messages as JSON"""
		messages = Message.query.order_by(Message.created_at.desc()).all()
		messages_data = []
		for msg in messages:
			messages_data.append({
				'id': msg.id,
				'name': msg.name,
				'email': msg.email,
				'message': msg.message,
				'created_at': msg.created_at.isoformat(),
				'formatted_date': msg.created_at.strftime('%B %d, %Y at %I:%M %p')
			})
		return {'messages': messages_data, 'total': len(messages_data)}

	@app.route("/messages")
	def messages_page():
		"""Amazing messages page with read_messages.py integration"""
		return render_template("messages_system.html")

	return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)