import csv
import sqlite3


def dump_with_filter(venues_path: str, csv_path: str):
    with open(venues_path) as venues_file:
        venues = []
        for line in venues_file:
            venues.append(line.strip())

        print("List of venues {}:".format(len(venues)))
        with open(csv_path) as csv_file:
            discarded_paper = []
            db_papers = []

            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                if row["num_pages"] == "nan" or row["num_pages"] == "":  # or len(row["abstract"].split(" ")) < 10:
                    row["num_pages"] = 0
                if int(row["num_pages"]) > 6 or int(row["num_pages"]) == 0:
                    csv_id = row["\ufeff"]
                    if row['doi'] == '':
                        doi = row['url']
                    else:
                        doi = "https://doi.org/" + row['doi']
                    if row["cleaned_publication_venue"].strip() in venues:
                        db_papers.append(
                            (csv_id, row['title'], row['authors'], row['venue'], row['abstract'], row['year'], doi, row['source']))
                # else:
                #     print(row["\ufeffid"])

            print("List of included papers {}:".format(len(db_papers)))
            print("List of discarded papers {}:".format(len(discarded_paper)))
            for paper in discarded_paper:
                print(paper)

    return db_papers


if __name__ == '__main__':

    db_papers = dump_with_filter("../final_venues.txt", "../final_paper_list.csv")

    db_1 = []
    db_2 = []
    db_3 = []
    for i in range(len(db_papers)):
        if i < len(db_papers) / 3 * 1:
            db_1.append(db_papers[i])
        elif i < len(db_papers) / 3 * 2:
            db_2.append(db_papers[i])
        else:
            db_3.append(db_papers[i])

    print("User 1 {}".format(len(db_1)))
    print("User 2 {}".format(len(db_2)))
    print("User 3 {}".format(len(db_3)))

    conn = sqlite3.connect('instance/paper_select_1.sqlite')
    c = conn.cursor()

    c.executemany('INSERT INTO paper(csv_id, title, authors, venue, abstract, year, doi, source) VALUES (?,?,?,?,?,?,?,?)', db_1)
    conn.commit()
    conn.close()

    conn = sqlite3.connect('instance/paper_select_2.sqlite')
    c = conn.cursor()

    c.executemany('INSERT INTO paper(csv_id, title, authors, venue, abstract, year, doi, source) VALUES (?,?,?,?,?,?,?,?)', db_2)
    conn.commit()
    conn.close()

    conn = sqlite3.connect('instance/paper_select_3.sqlite')
    c = conn.cursor()

    c.executemany('INSERT INTO paper(csv_id, title, authors, venue, abstract, year, doi, source) VALUES (?,?,?,?,?,?,?,?)', db_3)
    conn.commit()
    conn.close()
