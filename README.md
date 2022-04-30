# win-watchd
Windows watchdog

This utility program helps in montioring a folder which is created using python watchdog library. The logs of the montioring information is stored in logs.csv file.

To run the program, first clone the repo using 

```
git clone https://github.com/codfury/win-watchd.git
````
Then install the requirements.txt packages using:

```
pip install requirements.txt
````
Then run the wwatched.pyw file in terminal using

```
pythonw wwatched.pyw "C:\path\to\your\folder\to\be\monitored"
````
If the path isnt mentioned then it will watch the default folder <strong>watched</strong> in the repo.

You can view log of the changes to the mentioned folder in logs.csv.<br>
Then to stop the process type:
```
TASKKILL /F /IM pythonw.exe
````
