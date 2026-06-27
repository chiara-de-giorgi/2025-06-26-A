import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._idMapC={}

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1, year2):
        self._graph.clear()
        nodes=DAO.getAllCircuits()
        DAO.getResultsCircuitYear(self._idMapC, year1, year2)
        self._graph.add_nodes_from(nodes)

        for n in nodes:
            self._idMapC[n.circuitId]=n

        edges=DAO.getAllEdges(self._idMapC, year1, year2)
        for e in edges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)

    def getMaxCompConn(self):
        compConn = max(nx.connected_components(self._graph), key=len)
        maxCompConn = []
        for c in compConn:
            pesoMax=0
            for n in self._graph.neighbors(c):
                peso=self._graph[c][n]['weight']
                if peso > pesoMax:
                    pesoMax=peso
            maxCompConn.append((c, pesoMax))

        maxCompConn.sort(key=lambda x: x[1], reverse=True)
        return maxCompConn


    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getCircuitiEmozionati(self, M, k):
        self._bestCirc=[]
        self._bestImpr=0

        compConnessa = max(nx.connected_components(self._graph), key=len)
        nodiValidi=[]
        for n in compConnessa:
            if len(n.results.keys())>=M:
                nodiValidi.append(n)


        parziale=[]
        for n in nodiValidi:
            parziale=[n]
            self._ricorsione(nodiValidi, k, parziale)
        return self._bestCirc, self._bestImpr


    def _ricorsione(self, nodiValidi, k, parziale):
        #1) Caso terminale
        if len(parziale ) == k:
            imprevedibilita=self._getImprevedibilita(parziale)
            if imprevedibilita > self._bestImpr:
                self._bestImpr=imprevedibilita
                self._bestCirc=copy.deepcopy(parziale)
            return

        for n in nodiValidi:
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(nodiValidi, k, parziale)
                parziale.pop()

    def _getImprevedibilita(self, path):
        impr=0
        for circuito in path:
            nP = 0
            nPtot = 0
            for r in circuito.results.values():
                nPtot += len(r)
                for p in r:
                    if p[1] is not None: #P è una tupla con id del driver e posizione
                        nP+=1

            if nPtot>0:
                impr+= 1 - nP / nPtot
        return impr

