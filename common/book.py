import json
import csv
import re

YEAR_REGEX = re.compile('[^\d]*(\d{4})[^\d]*')


class Book:
    def __init__(self,
                 title: str,
                 description: str,
                 authors: str,
                 publisher: str,
                 year: str,
                 categories: list):
        self.title = title
        self.description = description
        self.authors = authors
        self.publisher = publisher
        self.year = year
        self.categories = categories

    @staticmethod
    def from_csv_row(csv_row: str):
        # Title,description,authors,image,previewLink,publisher,publishedDate,infoLink,categories,ratingsCount
        fields = list(csv.reader([csv_row]))[0]
        title = fields[0].strip()
        description = fields[1].strip()
        authors = fields[3].strip()
        publisher = fields[5].strip()
        year = Book.extract_year(fields[6].strip())
        categories = Book.extract_categories(fields[8].strip())
        return Book(title, description, authors, publisher, year, categories)

    @staticmethod
    def extract_year(x: str):
        if x:
            result = YEAR_REGEX.search(x)
            return result.group(1) if result else None
        return None

    @staticmethod
    def extract_categories(x: str):
        if not x:
            return None
        try:
            return json.loads(x.replace("'", '"'))
        except json.JSONDecodeError:
            return None

    def encode(self):
        return json.dumps([self.title, self.description, self.authors,
                           self.publisher, self.year, self.categories])

    @staticmethod
    def decode(data: str):
        fields = json.loads(data)
        title = fields[0]
        description = fields[1]
        authors = fields[2]
        publisher = fields[3]
        year = fields[4]
        categories = fields[5]
        return Book(title, description, authors, publisher, year, categories)

    def __str__(self):
        return self.encode()

    def filter_by(self, field: str, values: list):
        if field == 'title':
            return self.title in values
        if field == 'author':
            return self.author in values
        if field == 'year' and self.year is not None:
            return self.year in values
        if field == 'categories' and self.categories is not None:
            for category in self.categories:
                if category in values:
                    return True
        return False
