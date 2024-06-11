# lib/review.py
from __init__ import CURSOR, CONN

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
        Update object id attribute using the primary key value of new row."""
        sql = """
            INSERT INTO reviews (year, summary, employee_id)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance, save it to the database, and return the instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        """Return a Review instance having the attribute values from the table row."""
        review = cls(row[1], row[2], row[3])
        review.id = row[0]
        cls.all[review.id] = review
        return review

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance corresponding to the table row matching the specified primary key."""
        sql = """
            SELECT *
            FROM reviews
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql = """
            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Review instance."""
        sql = """
            DELETE FROM reviews
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]

    @classmethod
    def get_all(cls):
        """Return a list of Review instances for every record in the database."""
        sql = """
            SELECT *
            FROM reviews
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

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
