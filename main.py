from flask import Flask, render_template # importing the necessary Flask dependencies
import random # importing random for the Flask port 
import pandas as pd # importing pandas so fetch, sort, and calculate data from tables
import numpy as np # imporing numpy to identify 'nan'

app = Flask(__name__) # defining our app

def get_offer():
  df = pd.read_html('https://questionnaire-148920.appspot.com/swe/data.html') # reading the given url for tables
  df = df[0] # fetching the first graph found
  df['Salary'] = df['Salary'].str.replace(',', '', regex=False) # removing commas
  df['Salary'] = df['Salary'].str.replace('$', '', regex=False) # removing the dollar sign(s)
  df = df[df['Salary'] != 'no salary data'] # removing any value that displays 'no salary data'
  df = df[df['Salary'] != np.nan] # removing any value that outputs 'nan'
  df['Salary'] = pd.to_numeric(df['Salary']) # converting all values in the salary column to a number
  maximum = df['Salary'].nlargest(125, 'all').max() # fetching the largest salary
  lowest = df['Salary'].nlargest(125, 'all').min() # fetching the lowest salary within the 125 highest salaries found
  minimum = df['Salary'].min() # fetching the lowest salary of all
  data = df['Salary'].nlargest(125, 'all').mean() # calculating the average salary of the given 125 salaries
  offer = "${:,}".format(round(data)) # formatting all data with commas and dollar signs for better readability
  maximum = "${:,}".format(round(maximum))
  minimum = "${:,}".format(round(minimum))
  lowest = "${:,}".format(round(lowest))
  final_result = {
    "offer": offer, 
    "min": minimum, 
    "max": maximum, 
    "lowest_of": lowest
    } # defining every item in a dict
  return final_result

@app.errorhandler(500) # internal error handler 
def internal_server_error(e):
    return render_template('500.html'), 500 # returning this webpage on an internal server error

@app.errorhandler(404) # page not found error handler
def page_not_found(e):
  return render_template('404.html'), 404 # returning this webpage on 404 error

@app.route("/")
def home():
  offer = get_offer() # running the function and retrieving the dict accordingly
  return render_template("index.html", offer=offer) # rendering 'index.html' with the data included

if __name__ == "__main__": # running the flask app
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000))