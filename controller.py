from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QDate

class Controller:
    def __init__(self,model,view):
        self._model = model 
        self._view = view
        self.setup()

    def setup(self):
        # Plotting and picker funcionality
        self._view.setPlotButton.clicked.connect(self.setPlotButtonPushed)
        self.currencies = self._model.getCurrencies()
        names = [item['description'] for item in self.currencies]
        self._view.currencyPicker.addItems(names)

        # Exchange rates table data load 
        self.exRatesData = self._model.parseLatest()
        self._view.exRatesTable.setRowCount(len(self.exRatesData))
        self.loadTableData(self.exRatesData)


    def loadTableData(self,data):
        for i,(key,value) in enumerate(data.items()):
            self._view.exRatesTable.setItem(i,0, QTableWidgetItem(key))
            self._view.exRatesTable.setItem(i,1, QTableWidgetItem(str(value)))
        self._view.exRatesTable.resizeColumnsToContents()
        self._view.exRatesTable.resizeRowsToContents() 

    # Plot button handler
    def setPlotButtonPushed(self):
        toDate = self._view.toDatePicker.date().toPyDate()
        fromDate = self._view.fromDatePicker.date().toPyDate()
        daysDifference = (toDate - fromDate).days
        
        # API requirement -> Input checking from the controller point to avoid 
        # unnecessary failed requests
        if daysDifference > 365:
            self._view.setDateMsge.setVisible(True)
        elif daysDifference <= 0:
            self._view.setDateMsge.setText('"To Date" should refer to a later date than "From Date"')
            self._view.setDateMsge.setVisible(True)
        elif self._view.toDatePicker.date().toPyDate() > QDate.currentDate().toPyDate():
            self._view.setDateMsge.setText('"To Date" should not be greater than current date')
            self._view.setDateMsge.setVisible(True)
        else: 
            # Not an error -> ErrMsge not visible:
            self._view.setDateMsge.setVisible(False)
            
            # Index of picked currency:
            ind = [self.currencies.index(dict) for dict in self.currencies if dict['description']==self._view.currencyPicker.currentText()]
           
            # Necessary data for request:
            currency = self.currencies[ind[0]]['code']
            base = self._view.basePicker.currentText()
            fromDate = self._view.fromDatePicker.date()
            toDate = self._view.toDatePicker.date()
            tsreq = {'base':base,'currency':currency,'fromDate':fromDate,'toDate':toDate}
            
            # Request-> Parse -> Plot
            timeSeries = self._model.parseTimeSeries(tsreq,'timeSeries')
            x = range(len(timeSeries[1]))
            self._view.timeSPlot.clear()
            self._view.timeSPlot.plot(x,timeSeries[1],pen=self._view.timeSPen)


    
        