from database.DB_connect import DBConnect
from model.Arco import Arco
from model.circuit import Circuit


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct year
                    from seasons
                    order by year"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row['year'])

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct c.*
                from circuits c"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(row['circuitId'],
                               row['circuitRef'],
                               row['name'],
                               row['location'],
                               row['country'],
                               row['lat'],
                               row['lng'],
                               row['alt'],
                               row['url'],
                               {}))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getResultsCircuitYear(idMapC, year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r.circuitId as c, r.year, s.driverId, s.position
                from races r, results s
                where r.raceId= s.raceId and r.year >= %s and r.year<=%s
"""
        cursor.execute(query, (year1, year2, ))

        res = []
        for row in cursor:
            if row['c'] not in idMapC:
                continue

            circuit= idMapC[row['c']]
            year=row['year']
            if year not in circuit.results:
                circuit.results[year]=[]
            circuit.results[year].append((row['driverId'], row['position']))

        cursor.close()
        cnx.close()
        return res


    @staticmethod
    def getAllEdges(idMapC, year1, year2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct c1.circuitid as c1, c2.circuitid as c2, p1 + p2 as peso
                    from (select r.circuitId, count(s.driverId ) as p1
                            from results s, races r
                            where r.raceId= s.raceId and r.year >= %s and r.year<=%s
                            and s.position is not null
                            group by r.circuitId 
                            ) c1,
                    (select r.circuitId, count(s.driverId ) as p2
                            from results s, races r
                            where r.raceId= s.raceId and r.year >= %s and r.year<=%s
                            and s.position is not null
                            group by r.circuitId 
                            ) c2
                    where c1.circuitid < c2.circuitid """

        cursor.execute(query, (year1, year2, year1, year2))

        res = []
        for row in cursor:
            c1=idMapC[row['c1']]
            c2=idMapC[row['c2']]
            peso=row['peso']
            res.append(Arco(c1, c2, peso))

        cursor.close()
        cnx.close()
        return res