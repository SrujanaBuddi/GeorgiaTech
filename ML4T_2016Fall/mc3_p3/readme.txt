Place indicators.py,rule_based.py and ML_based.py in a folder
To get the indicators, in command window from the current directory of file run 
python indicators.py
The above command will generate five images and save them in current folder

------------------------------------------------------------------------------------------------------------------------------------------------

To run the rule based strategy model, in command window from the current directory run
python rule_based.py

to get orders for training data, in the main function of rule_based.py set sd as dt.datetime(2006,01,01) and ed as dt.datetime(2009,12,31) and to get orders for testing data set sd as dt.datetime(2010,01,01) and ed as dt.datetime(2010,12,31)
This model creates orders file with name rule_based_output.csv

------------------------------------------------------------------------------------------------------------------------------------------------

To run the ML based strategy model, in command window from the current directory run
python ML_based.py

to get orders for training data, in the main function of ML_based.py set test_sd as dt.datetime(2006,01,01) and test_ed as dt.datetime(2009,12,31) and to get orders for testing data set test_sd as dt.datetime(2010,01,01) and test_ed as dt.datetime(2010,12,31)
This model creates orders file with name ml_output.csv
