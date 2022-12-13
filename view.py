### This class only handles the view/graphic side of the app, the actual functionality
### is handled by the controller and model, as expected from this Design Pattern.
### With that said, button actions will be defined in the controller, and here we only
### refer to its layout.

from xml.etree.ElementTree import tostring
from PyQt5 import QtGui
from PyQt5.QtCore import Qt,QDateTime,QDate,QTimer
from PyQt5.QtWidgets import QMainWindow,QTableWidget,QHBoxLayout,QVBoxLayout,QWidget, QLabel,QGridLayout,QGroupBox,QDateEdit,QPushButton,QSizePolicy,QComboBox,QTabWidget
import pyqtgraph as pqtg
from pyqtgraph import PlotWidget, plot
from pyqtgraph.Qt import QtGui

class View(QMainWindow):

    def __init__(self):
        super(View,self).__init__()
        self.initUi()
       
    def initUi(self):
        self.setWindowTitle("Currency App")
        self.setFixedSize(1200,650)
        self.pickerfont = QtGui.QFont('Calibri',13)
               
        self.boxesArraySetUp()

        self.centerWidgetSetUp()        
        self.show()

    def tabsInit(self):
        self.timeSTab = QTabWidget()
        self.ratesTab = QTabWidget()

        self.timeSerTab = QWidget()
        self.fluctuationTab = QWidget()
        self.exchangeRTab = QWidget()
        self.historicalRTab = QWidget()

        self.tabfont = QtGui.QFont('Calibri',13)
        self.timeSTab.setFont(self.tabfont)
        self.ratesTab.setFont(self.tabfont)
        self.ratesTab.setFixedWidth(300)
        
        self.timeSTab.addTab(self.timeSerTab,'Time series rates')
        self.timeSTab.addTab(self.fluctuationTab,'Fluctuation data')
        self.ratesTab.addTab(self.exchangeRTab,'Exchange rates')
        self.ratesTab.addTab(self.historicalRTab,'Historical rate')
    
    def timeSeriesPlotInit(self):
        self.timeSPlot = PlotWidget()
        self.timeSPlot.setLabel('bottom','Days',self.pickerfont)
        self.timeSPlot.setLabel('left','Rate',self.pickerfont)
        self.timeSPen = pqtg.mkPen(color=(79,112,246),width=4)
        self.timeSPlot.showGrid(True,True,0.5)

    def currencyPickerSetUp(self):
        self.currencyPicker = QComboBox()
        self.currencyPicker.setFont(self.pickerfont)
        self.currencyPicker.setSizeAdjustPolicy(QComboBox.AdjustToContents)

    def datePickersSetUp(self):
        self.fromDatePicker = QDateEdit(self)
        self.fromDatePicker.setFixedHeight(40)
        self.fromDatePicker.setFixedWidth(500)
        self.fromDatePicker.setFont(self.pickerfont)
        self.fromDatePicker.setDate(QDate(2020,10,10))
        self.toDatePicker = QDateEdit(self)
        self.toDatePicker.setFixedHeight(40)
        self.toDatePicker.setFixedWidth(500)
        self.toDatePicker.setFont(self.pickerfont)
        self.toDatePicker.setDate(QDate(2020,10,10))

    def plotButtonSetUp(self):
        self.setPlotButton = QPushButton('PLOT',self)
        self.setPlotButton.setFont(self.pickerfont)
        self.setPlotButton.setFixedHeight(40)
        self.setPlotButton.setFixedWidth(100)

    def dateErrMsgeSetUp(self):    
        self.setDateMsge = QLabel()
        self.pickerfont.setBold(True)
        self.setDateMsge.setFont(self.pickerfont)
        self.setDateMsge.setFixedHeight(70)
        self.setDateMsge.setFixedWidth(200)
        self.setDateMsge.setWordWrap(True)
        self.setDateMsge.setText('Maximum time interval allowed: 365 days!')
        self.setDateMsge.setStyleSheet("color:rgb(255,49,49)")
        dmsgeSizePol = QSizePolicy()
        dmsgeSizePol.setRetainSizeWhenHidden(True)
        self.setDateMsge.setSizePolicy(dmsgeSizePol)
        self.setDateMsge.setVisible(False)   

    def hboxCurrPickerSetUp(self):
        currencyLabel = QLabel()
        currencyLabel.setText('Currency:')
        currencyLabel.setFont(self.pickerfont)
        self.currencyPickerSetUp()        
        
        baseLabel = QLabel()
        baseLabel.setText('Base:')
        baseLabel.setFont(self.pickerfont)
        self.basePicker = QComboBox()
        self.basePicker.setFont(self.pickerfont)
        bases = ['USD','EUR']
        self.basePicker.addItems(bases)
        self.basePicker.setFixedWidth(80)

        hboxCurrencyPicker = QHBoxLayout()
        hboxCurrencyPicker.addWidget(baseLabel)
        hboxCurrencyPicker.addWidget(self.basePicker) 
        hboxCurrencyPicker.addWidget(currencyLabel)
        hboxCurrencyPicker.addWidget(self.currencyPicker)
        hboxCurrencyPicker.addStretch()       
        return hboxCurrencyPicker

    def hboxDatePickersSetUp(self):
        self.datePickersSetUp()         
        fromLabel = QLabel()
        fromLabel.setText('From:')
        fromLabel.setFont(self.pickerfont)
        toLabel = QLabel()
        toLabel.setText('To:')
        toLabel.setFont(self.pickerfont)

        # Setting Plot Button
        self.plotButtonSetUp()

        # API requires time interval less than 365 days - This is an error msge:
        self.dateErrMsgeSetUp()

        # Setting labels/date pickers/error msges in HBox
        hboxDatePickers = QHBoxLayout()
        hboxDatePickers.addWidget(fromLabel)
        hboxDatePickers.addWidget(self.fromDatePicker)
        hboxDatePickers.addWidget(toLabel)
        hboxDatePickers.addWidget(self.toDatePicker)
        hboxDatePickers.addSpacing(30)
        hboxDatePickers.addWidget(self.setPlotButton)
        hboxDatePickers.addWidget(self.setDateMsge)
        hboxDatePickers.addStretch()   

        return hboxDatePickers
   
    def boxesArraySetUp(self): 
        # Tabs are organized in two pairs, one for historical rate/exchange rates 
        # and other for Time series exchange rates/Fluctuation data
        # Setting up table with exchange rates
        self.tabsInit() 
    
        self.exRatesTable = TableView()
        vbox = QVBoxLayout()
        vbox.addSpacing(10)
        vbox.addWidget(self.exRatesTable)
        self.exchangeRTab.setLayout(vbox)
        self.exchangeRTab.setFixedSize(300,500)

        # Setting base currency picker/currency picker/labels in hbox
        hboxCurrencyPicker = self.hboxCurrPickerSetUp()

        # Setting up date pickers menus
        hboxDatePickers = self.hboxDatePickersSetUp()
        
        # Data plot. It will displayed when user picks the options and pushes the Plot button 
        self.timeSeriesPlotInit() 

        # Combining it into a widget -> Layout -> and then to the Tab layout 
        DatePickerWidget = QWidget()
        DatePickerWidget.setLayout(hboxDatePickers)
        currencyPickerWidget = QWidget()
        currencyPickerWidget.setLayout(hboxCurrencyPicker)
        vboxTimeSeries = QVBoxLayout()
        vboxTimeSeries.addWidget(currencyPickerWidget)
        vboxTimeSeries.addWidget(DatePickerWidget)
        vboxTimeSeries.addWidget(self.timeSPlot)
        vboxTimeSeries.addStretch()
        self.timeSerTab.setLayout(vboxTimeSeries) 
        self.timeSerTab.setFixedHeight(500)

        # Header files(hboxMain) -> time,date,location
        # vboxMain -> Tabs
        self.vboxMain = QVBoxLayout()
        hboxMain = QHBoxLayout()
        
        # Clock label setting
        self.clockWidget = Clock()

        # Header set up
        hboxMain.addStretch()
        hboxMain.addWidget(self.clockWidget)
        hBoxWidget = QWidget()
        hBoxWidget.setLayout(hboxMain)
        
        # Highest hierarchy box -> mainWindow view
        self.vboxMain.addWidget(hBoxWidget)
        hboxTabsDisplay = QHBoxLayout() 
        hboxTabsDisplay.addWidget(self.ratesTab)
        hboxTabsDisplay.addWidget(self.timeSTab)
        
        # hbox of Tabs -> As Widget -> mainWindow 
        hboxTabsWidget = QWidget()
        hboxTabsWidget.setLayout(hboxTabsDisplay)
        self.vboxMain.addWidget(hboxTabsWidget)

    def centerWidgetSetUp(self):
        # Setting up the view as the central widget of main window 
        centralWidg = QWidget()
        centralWidg.setLayout(self.vboxMain)
        self.setCentralWidget(centralWidg)

class TableView(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setFont(QtGui.QFont('Arial',14))
        self.setHorizontalHeaderLabels(['Currency','Rate[EUR]'])

class Clock(QLabel):
    def __init__(self):
        super().__init__() 
        timer = QTimer(self)
        timer.timeout.connect(self.updateTime)
        timer.start(1000)
        font = QtGui.QFont('Calibri',16,QtGui.QFont.Bold)
        self.setFont(font)
    
    def updateTime(self):
        self.setText((QDateTime.currentDateTime()).toString(Qt.DefaultLocaleLongDate))


