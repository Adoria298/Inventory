import sqlite3

class ScoresDB:
    def __init__(self) -> None:
        self.operas = ("Trial by Jury", "The Sorcerer", "HMS Pinafore", "The Pirates of Penzance", "Patience", "Iolanthe", "Princess Ida", "The Mikado", "Ruddigore", "The Yeomen of the Guard", "The Gondoliers", "Utopia, Limited", "The Grand Duke", "The Zoo", "Cox and Box")
        self.score_types = ("Full Score", "Vocal Score", "Instrumental Part", "Other")
        self.locations = ("Phoenix", "Sam", "Cupboard")
        self.con = sqlite3.connect("./ScoresDB.db")
        self.cur = self.con.cursor()
        self.init_db()
        self.populate_db()
        self.cur.execute("""SELECT scores.tag, operas.opera, scores.condition, score_types.type, editions.name, locations.location 
                         FROM scores
                         INNER JOIN operas ON scores.opera_id = operas.id
                         INNER JOIN score_types ON scores.type_id = score_types.id
                         INNER JOIN editions ON scores.edition_id = editions.id
                         INNER JOIN locations ON scores.location_id = locations.id""")
        print(self.cur.fetchall())


    def init_db(self):    
        self.cur.execute("""CREATE TABLE IF NOT EXISTS operas (id INTEGER PRIMARY KEY, opera TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS score_types (id INTEGER PRIMARY KEY, type TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS locations (id INTEGER PRIMARY KEY, location TEXT, description TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS editions (id INTEGER PRIMARY KEY,
                                                        opera_id INTEGER,
                                                        type_id INTEGER,
                                                        name TEXT,
                                                        pagecount INTEGER,
                                                        isbn TEXT,
                                                        FOREIGN KEY (opera_id) REFERENCES opera(id),
                                                        FOREIGN KEY (type_id) REFERENCES book_types(id))""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY,
                                                        opera_id INTEGER,
                                                        tag TEXT,
                                                        condition TEXT,
                                                        notes TEXT,
                                                        type_id INTEGER,
                                                        edition_id INTEGER,
                                                        location_id INTEGER,
                                                        FOREIGN KEY (opera_id) REFERENCES opera(id),
                                                        FOREIGN KEY (type_id) REFERENCES book_types(id),
                                                        FOREIGN KEY (edition_id) REFERENCES editions(id),
                                                        FOREIGN KEY (location_id) REFERENCES locations(id))""")
        
        self.cur.execute("""CREATE TABLE IF NOT EXISTS libretti (id INTEGER PRIMARY KEY,
                                                        opera_id INTEGER,
                                                        tag TEXT,
                                                        condition TEXT,
                                                        notes TEXT,
                                                        edition_id INTEGER,
                                                        location_id INTEGER,
                                                        FOREIGN KEY (opera_id) REFERENCES opera(id),
                                                        FOREIGN KEY (edition_id) REFERENCES editions(id),
                                                        FOREIGN KEY (location_id) REFERENCES locations(id))""")       
        

        
    def populate_db(self) -> None:
        for opera in self.operas:
            self.cur.execute(f"INSERT INTO operas (opera) VALUES ('{opera}')")

        for score_type in self.score_types:
            self.cur.execute(f"INSERT INTO score_types (type) VALUES ('{score_type}')")

        self.cur.execute("INSERT INTO locations (location) VALUES ('Phoenix')")
        self.cur.execute(f"INSERT INTO editions (opera_id, name) VALUES ({self.operas.index('Princess Ida')+1}, 'D''Oyly Carte (Edwards 1998)')")

        self.cur.execute(f"INSERT INTO scores (opera_id, tag, condition, type_id, edition_id, location_id) VALUES ({self.operas.index('Princess Ida')+1}, 'PI-0', 'Good', {self.score_types.index('Full Score')+1}, 1, {self.locations.index('Phoenix')+1})")
        

    def count_scores(self, opera: str) -> str:
        self.cur.execute(f"SELECT count(*) FROM scores WHERE opera_id='{self.operas.index(opera)+1}'")
        return self.cur.fetchall()[0][0] # should be only one value on one row

if __name__ == "__main__":
    sdb = ScoresDB()
    print(sdb.count_scores("Princess Ida"))
    # vitally important steps!!
    sdb.cur.close()
    sdb.con.close()
            