import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._year1Value=None
        self._year2Value= None

    def handleBuildGraph(self, e):
        year1=int(self._year1Value)
        year2=int(self._year2Value)
        print(year1, year2)
        if year1 is None or year2 is None:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(ft.Text("Selezionare un range di anni dall'apposito dropdown!", color="red"))
            self._view.update_page()
            return

        if year1 > year2:
            self._view._txtGraphDetails.controls.clear()
            self._view._txtGraphDetails.controls.append(
                ft.Text("Selezionare un range di anni valido dall'apposito dropdown!", color="red"))
            self._view.update_page()
            return

        self._view._txtGraphDetails.controls.clear()
        self._model.buildGraph(year1, year2)
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo correttamente creato."))
        n, a =self._model.getGraphDetails()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Il grafo contiene {n} nodi e {a} archi."))
        self._view.update_page()

    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("Stampa dettagli:"))
        maxCompConnessa=self._model.getMaxCompConn()
        for c, peso in maxCompConnessa:
            self._view._txtGraphDetails.controls.append(ft.Text(f"{c} -- {peso}"))
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        self._view._txtGraphDetails.controls.clear()
        self._view._txt_result.controls.clear()
        M=self._view._txtInSoglia.value
        k=self._view._txtInNumDiEdizioni.value

        if k=="" or k is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire il numero di gare per procedere!", color="red"))
            self._view.update_page()
            return

        if M=="" or M is None:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire la soglia di anni per procedere!", color="red"))
            self._view.update_page()
            return

        try:
            intK=int(k)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero di gare per procedere!", color="red"))
            self._view.update_page()
            return

        try:
            intM= int(M)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Inserire un numero intero per la soglia di anni per procedere!", color="red"))
            self._view.update_page()
            return

        if intM <=0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un numero intero positivo per la soglia di anni per procedere!", color="red"))
            self._view.update_page()
            return

        if intK<=0:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(
                ft.Text("Inserire un numero intero positivo di gare per procedere!", color="red"))
            self._view.update_page()
            return

        bestCircuito, bestImpr= self._model.getCircuitiEmozionati(intM, intK)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Il sotto-campionato più interessante trovato svolto in {k} edizioni"
                                                       f"in cui si è corso almeno {M} volte ha avuto un'imprevedibilià del {bestImpr}"))
        for n in bestCircuito:
            self._view._txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def fillDDYear(self):
        year=self._model.getAllYears()
        year1DDOptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDYear1), year))
        year2DDOptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceDDYear2), year))
        self._view._ddYear1.options = year1DDOptions
        self._view._ddYear2.options = year2DDOptions
        self._view.update_page()

    def _choiceDDYear1(self, e):
        self._year1Value = e.control.data

    def _choiceDDYear2(self, e):
        self._year2Value = e.control.data





