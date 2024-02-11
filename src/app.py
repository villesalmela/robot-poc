"""A small Flask application for logging voting stats and incidents per polling station."""

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

DATABASE = "data.db"


def get_db_connection():
    """Return a connection to the database."""

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database by creating the empty tables."""

    conn = get_db_connection()
    conn.executescript("""
                    DROP TABLE IF EXISTS voters;
                    DROP TABLE IF EXISTS incidents;
                    
                    CREATE TABLE IF NOT EXISTS voters
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     polling_station_name TEXT NOT NULL,
                     polling_station_id INTEGER NOT NULL,
                     number_of_voters INTEGER NOT NULL);
                 
                    CREATE TABLE IF NOT EXISTS incidents
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     polling_station_name TEXT NOT NULL,
                     polling_station_id INTEGER NOT NULL,
                     incident_type TEXT NOT NULL,
                     incident_description TEXT NOT NULL)""")
    conn.commit()
    conn.close()


app = Flask(__name__)
with app.app_context():
    init_db()


@app.route("/")
def index():
    """Display the main page."""

    return render_template("index.html")


@app.route("/voters", methods=["GET", "POST"])
def voters():
    """Handle the display and submission of the voters form."""

    form_fields = [
        {
            "name": "Polling Station Name",
            "placeholder": "for example Suutarila",
            "type": "text"
        },
        {
            "name": "Polling Station ID",
            "placeholder": "for example 85",
            "type": "number"
        },
        {
            "name": "Number of Voters",
            "placeholder": "for example 2700",
            "type": "number"
        }
    ]
    if request.method == "POST":
        polling_station_name = request.form["Polling Station Name"]
        polling_station_id = request.form["Polling Station ID"]
        number_of_voters = request.form["Number of Voters"]
        conn = get_db_connection()
        conn.execute("""INSERT INTO voters (
                        polling_station_name,
                        polling_station_id,
                        number_of_voters
                     ) VALUES (?, ?, ?)""",
                     (polling_station_name, polling_station_id, number_of_voters)
                     )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("form.html.j2",
                           form_action=url_for("voters"),
                           form_title="Log Voters",
                           form_fields=form_fields)


@app.route("/incident", methods=["GET", "POST"])
def incident():
    """Handle the display and submission of the incident form."""

    form_fields = [
        {
            "name": "Polling Station Name",
            "placeholder": "for example Suutarila",
            "type": "text"
        },
        {
            "name": "Polling Station ID",
            "placeholder": "for example 85",
            "type": "number"
        },
        {
            "name": "Incident Type",
            "placeholder": "Select one",
            "type": "radio",
            "options": ["Security", "Policy Violation", "Fraud", "Other"]
        },
        {
            "name": "Incident Description",
            "placeholder": "More details",
            "type": "textarea"
        }
    ]
    if request.method == "POST":
        polling_station_name = request.form["Polling Station Name"]
        polling_station_id = request.form["Polling Station ID"]
        incident_type = request.form["Incident Type"]
        incident_description = request.form["Incident Description"]

        conn = get_db_connection()
        conn.execute("""INSERT INTO incidents (
                        polling_station_name,
                        polling_station_id,
                        incident_type,
                        incident_description
                     ) VALUES (?, ?, ?, ?)""",
                     (polling_station_name, polling_station_id,
                      incident_type, incident_description)
                     )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("form.html.j2",
                           form_action=url_for("incident"),
                           form_title="Log an Incident",
                           form_fields=form_fields)


if __name__ == "__main__":
    app.run()
