# zoom_attendance

Please put your input zoom attendance files in the inputCSV folder.
$ python3 -i load_csv.py

--------About input file name----------
You must start your file name with section letter in capital, and whatever comes behind.

--------To create a new report from lab1----------
1.  Enter the input csv file's name only
2.  If this is the first input, do not enter anything for the "Enter the previous section existing CSV filename"
3.  Enter Section: Either B or C
4.  Output file will be dumped at outputCSV

--------To generate a new report based on previous labs----------
1.  Enter the input csv file's name only
2.  Exact match of previous version's file name except for .csv
3.  Enter Section: Either B or C
4.  Output file will be dumped at outputCSV

--------About output file name---------
All files start with section letter followed by a dash and lab and number
For example: B-lab1.csv where B is the section, lab1 means this report contains upto lab1's attendance

--------For future FLASK_APP---------
On Mac/Linux
$ . venv/bin/activate
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/

On Windows:
> venv\Scripts\activate
$ export FLASK_APP=hello.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/
