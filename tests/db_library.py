"""Module for interacting with the database from Robot Framework."""

import sqlite3


class db_library: # pylint: disable=invalid-name
    """Class for retrieving voter stats and incident reports from the database."""

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def get_voter_data(self, polling_station_id):
        """Return the number of voters and the name of the polling station,
            given the polling station ID."""

        self.cursor.execute("""
                            SELECT
                                polling_station_name,
                                number_of_voters
                            FROM
                                voters
                            WHERE
                                polling_station_id = ?
                            """,
                            (polling_station_id,)
                            )
        return self.cursor.fetchone()

    def get_incident_data(self, polling_station_id):
        """Return the incident type and description, given the polling station ID."""

        self.cursor.execute("""
                            SELECT
                                polling_station_name,
                                incident_type,
                                incident_description
                            FROM
                                incidents
                            WHERE
                                polling_station_id = ?
                            """,
                            (polling_station_id,)
                            )
        return self.cursor.fetchone()
