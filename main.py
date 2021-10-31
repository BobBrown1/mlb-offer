# importing the necessary libraries for the project
from flask import Flask, render_template 
import random
import pandas as pd 
import numpy as np

# defining our app
app = Flask(__name__)

def get_offer():
   # reading the given url for tables
  df = pd.read_html('https://questionnaire-148920.appspot.com/swe/data.html')

  # fetching the first graph found
  df = df[0] 

  # removing commas and dollar signs in each value
  df['Salary'] = df['Salary'].str.replace(',', '', regex=False)
  df['Salary'] = df['Salary'].str.replace('$', '', regex=False)

  # removing any value that displays 'no salary data' or is 'nan'
  df = df[df['Salary'] != 'no salary data'] 
  df = df[df['Salary'] != np.nan]

  # attempting to convert all values to numeric and returning error template if it fails
  try:
    df['Salary'] = pd.to_numeric(df['Salary'])
  except:
    return render_template("500.html", error="Unable to convert all values to numbers.")

  # fetching the largest salary
  maximum = df['Salary'].nlargest(125, 'all').max()

  # fetching the lowest salary within the 125 highest salaries found
  lowest = df['Salary'].nlargest(125, 'all').min()

  # fetching the lowest salary of all
  minimum = df['Salary'].min()

  # calculating the average salary of the given 125 salaries
  data = df['Salary'].nlargest(125, 'all').mean()

  # formatting all data with commas and dollar signs for better readability
  offer = "${:,}".format(round(data))
  maximum = "${:,}".format(round(maximum))
  minimum = "${:,}".format(round(minimum))
  lowest = "${:,}".format(round(lowest))

  # defining every item in a dict and returning it
  final_result = {
    "offer": offer, 
    "min": minimum, 
    "max": maximum, 
    "lowest_of": lowest
    }
  return final_result

# internal error handler 
@app.errorhandler(500)
def internal_server_error(e):

  # returning this webpage on an internal server error
  return render_template('500.html'), 500
  
# page not found error handler
@app.errorhandler(404) 
def page_not_found(e):

  # returning this webpage on 404 error
  return render_template('404.html'), 404

@app.route("/")
def home():
  # running the function and retrieving the dict accordingly
  offer = get_offer() 

  # rendering 'index.html' with the data included
  return render_template("index.html", offer=offer) 

# running the flask app
if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000))