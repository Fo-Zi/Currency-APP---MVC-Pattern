# Currency Application -> GUI design applying the MVC pattern
## Summary
In this application i try to demonstrate the application of the Model View Controller(MVC) design pattern. This pattern allow us to decouple very well the visualization or graphic side of our app from the functionality behind it. With that purpose i've used the API of a webpage to retrieve information(Model) that then will be displayed(View) in a user-friendly manner. The resources that i used are:
- [Exchange API](https://exchangerate.host/#/#docs)
- [PyQt5](https://doc.qt.io/qtforpython/)
- [Dark Stylesheet](https://github.com/ColinDuquesnoy/QDarkStyleSheet.git)
- [Plotting/Graphs](https://github.com/pyqtgraph/pyqtgraph)

This is how far the application is developed right now:

![alt text](https://github.com/Fo-Zi/Portfolio/blob/main/Python/GUI_MVC_Pattern/GUI_img.jpeg)
 
There are a lot of things that can be improved: Implementing error handling for the API in case the requests fail from the server-side, implementing the other two tabs functionality(Historical rate and fluctuation data), applying interfaces and abstract classes to create more generic code base could be of help in case one wants to reuse it for another design, etc. But i think this serves well as an MVC proof of concept using PyQt.
#### Thanks for pasing by!

## Build

To install the necessary dependencies, you can run:
```
pip install -r requirements.txt
```
Then you can test the application simply by running:
```
python3 app
```
