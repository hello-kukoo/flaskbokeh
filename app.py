# -*- coding: utf-8 -*-

from flask import Flask, Response, make_response, render_template, request

import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file
from bokeh.embed import components
from bokeh.charts import Histogram

app = Flask(__name__)

# Import dataset
data = pd.read_csv('data/gapminder.csv')
data = data[(data.Year >= 1950)]
country_names = sorted(list(set(data.Country)))
attribute_names = data.columns[2:-1].values.tolist()


# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.data",
            names=["Sepal Length", "Sepal Width", "Petal Length", "Petal Width", "Species"])
feature_names = iris_df.columns[0:-1].values.tolist()


# Index page
@app.route('/')
def index():
    return render_template('index.html')


# Create the main plot
def create_gapminder_figure(first_country='China',
                  second_country='Singapore',
                  selected_attribute='income'):

    # filter datasets according to country
    first_country_data = data[(data.Country == first_country)]
    second_country_data = data[(data.Country == second_country)]

    first_country_data_attribute = list(first_country_data[selected_attribute])
    second_country_data_attribute = list(second_country_data[selected_attribute])

    years = list(first_country_data["Year"])
    # output to static HTML file
    output_file("gapminder.html")

    # create a new plot
    p = figure(title="Country Data Analysis", x_axis_label='Years',
                width=1280, height=720)

    p.line(years, first_country_data_attribute, legend=first_country,
            line_color="blue", line_width=3)

    p.line(years, second_country_data_attribute, legend=second_country,
            line_color="green", line_width=3)
    return p


@app.route('/gapminder', methods=['GET', 'POST'])
def gapminder_plot():
    first_country = "China"
    second_country = "Singapore"
    selected_attribute = "income"
    if request.method == 'POST':
        first_country = request.form["first_country"]
        second_country = request.form["second_country"]
        selected_attribute = request.form["selected_attribute"]

    # Create the plot
    plot = create_gapminder_figure(first_country, second_country, selected_attribute)
    # Embed plot into HTML via Flask Render
    script, div = components(plot)

    return render_template("gapminder.html",
                           script=script,
                           div=div,
                           country_names=country_names,
                           attribute_names=attribute_names,
                           selected_attribute=selected_attribute,
                           first_country=first_country,
                           second_country=second_country)


# Create the iris plot
def create_iris_figure(current_feature_name, bins):
	p = Histogram(iris_df, current_feature_name,
        title=current_feature_name, color='Species',
	 	bins=bins, legend='top_right', width=600, height=400)

	# Set the x axis label
	p.xaxis.axis_label = current_feature_name

	# Set the y axis label
	p.yaxis.axis_label = 'Count'
	return p

@app.route('/iris', methods=['GET', 'POST'])
def iris_plot():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "Sepal Length"

    # Create the plot
    plot = create_iris_figure(current_feature_name, 10)
    script, div = components(plot)

    return render_template("iris.html",
                           script=script,
                           div=div,
                           feature_names=feature_names,
                           current_feature_name=current_feature_name)


# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)

