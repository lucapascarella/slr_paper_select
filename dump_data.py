import csv
import sqlite3

conn = sqlite3.connect('instance/paper_select.sqlite')

c = conn.cursor()

csv_path = 'papers.csv'
db_papers = []

with open(csv_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        db_papers.append((row['title'], row['authors'], row['venue'], row['abstract'], row['year'], row['doi'], row['source']))

c.executemany('INSERT INTO paper(title, authors, venue, abstract, year, doi, source) VALUES (?,?,?,?,?,?,?)', db_papers)
conn.commit()
conn.close()
