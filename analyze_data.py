from dash import Dash, html, dcc
import pandas as pd
import dash_ag_grid as dag
import plotly.express as px

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")

print("Dataframe Shape:", df.shape, '\n')

print("Dataframe Columns:", df.columns, '\n')

print("Dataframe Dtypes:\n", df.dtypes, '\n')

print("Dataframe Description:\n", df.describe(), '\n')

print("Dataframe Head:\n", df.head(), '\n')

print("Dataframe Tail:\n", df.tail(), '\n')

print("Missing Values in Dataframe:\n", df.isnull().sum(), '\n')

print("Unique Values per Column:\n", df.nunique(), '\n')

print("Dataframe Info:")
df.info()
print("\n")

print("Value Counts for 'continent' Column:\n", df['continent'].value_counts(), '\n')

app = Dash()

app.layout = [
	html.Div(
		children="Population and Life Expectancy by Continent in 2007", 
		style={"fontSize": 24, "margin": 10}),
	dag.AgGrid(
		id="population-lifeexp-grid",
		rowData=df.to_dict("records"),
		columnDefs=[{"field": col} for col in df.columns],
	),
	dcc.Graph(figure=px.histogram(df, x='continent', y = 'lifeExp', histfunc='avg'))
]

if __name__ == "__main__":
	app.run(debug=True)