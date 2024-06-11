# review.py

from __init__ import CURSOR, CONN
from employee import Employee  # Import Employee class here to avoid circular imports

class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        pass  # Implementation will be added later

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        pass  # Implementation will be added later
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        pass  # Implementation will be added later

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance corresponding to the table row matching the specified primary key"""
        pass  # Implementation will be added later

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        pass  # Implementation will be added later

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        pass  # Implementation will be added later

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        pass  # Implementation will be added later

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        if year < 2000:
            raise ValueError("Year must be greater than or equal to 2000")
        self._year = year

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, summary):
        if not isinstance(summary, str) or len(summary) == 0:
            raise ValueError("Summary must be a non-empty string")
        self._summary = summary
