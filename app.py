from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import dash_ag_grid as dag
import plotly.express as px

# Layout data
colors = {
	'background': "#E1F9F9",
	'table_background': "#FFFFFF",
	'table_text': "#2A98C3",
	'text': '#7FDBFF',
	'title': "#FD726A"
}

# Work on fruit data
fruits_df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(fruits_df, x="City", y="Amount", color="Fruit", barmode="group")
fig.update_layout(
	plot_bgcolor=colors['table_background'],
	paper_bgcolor=colors['table_background'],
	font_color=colors['table_text']
)

# Work on countries data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

agg_df = df.groupby('country').agg(
	pop_sum=('pop', 'sum'),
	pop_mean=('pop', 'mean'),
	lifeExp_mean=('lifeExp', 'mean'),
	gdpPercap_mean=('gdpPercap', 'mean'),
	years_count=('year', 'nunique'),
	first_year=('year', 'min'),
	last_year=('year', 'max')
).reset_index()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

print("Dataframe Columns:", df.columns, '\n')
print("Aggregated Dataframe Columns:", agg_df.columns, '\n')

# App layout
app.layout = [
	html.Div(
		style={'backgroundColor': colors['background']},
		children=[
			html.H1(
				children="Gapminder Data Explorer",
				style={
					'backgroundColor': colors['background'],
					'textAlign': 'center', 
					'margin': 10,
					'color': colors['title']
				}
			),
			html.Div(
				className='row',
				children = [
					html.Div(
						children=[
							'Select Country:',
							dcc.Dropdown(
								df.country.unique(),
								'Canada',
								id='dropdown-country'
							)
						]
					),
					html.Div(
						children=[ 
							'Select Metric:',
							dcc.RadioItems(
								options=[
									{'label': 'Population', 'value': 'population'},
									{'label': 'Life Expectancy', 'value': 'life expectancy'},
									{'label': 'GDP per Capita', 'value': 'gdp per capita'},
								],
								value='population',
								id='radio-metric'
							),
						]
					),
					html.Br(),
				]
			),
			dcc.Graph(id='graph-output'),
			dag.AgGrid(
				rowData=agg_df.to_dict('records'),
				columnDefs=[{"field": i} for i in agg_df.columns]
			),
			dcc.Graph(
				figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg')
			),
			html.Div(
				children=[
					html.H2(
						children="Fruit Amounts by City",
						style={"textAlign": "center"}
					), 
					dcc.Graph(
						id='fruits-graph',
						figure=fig
					)
				], 
				style={"fontSize": 24, "margin": 10}
			),
		]
	),
]

# Countries reactivity
@callback(
	Output('graph-output', 'figure'),
	Input('dropdown-country', 'value'),
	Input('radio-metric', 'value')
)
def countries_graph(selected_country, selected_metric):
	filtered_df = df[df.country == selected_country]

	# Map the dropdown selection to the DataFrame column name.
	metric_map = {
		'population': 'pop',
		'life expectancy': 'lifeExp',
		'gdp per capita': 'gdpPercap'
	}
	pretty_map = {
		'population': 'Population',
		'life expectancy': 'Life Expectancy',
		'gdp per capita': 'GDP per Capita'
	}
	metric_col = metric_map.get(selected_metric, 'pop')
	pretty = pretty_map.get(selected_metric, 'Population')

	fig = px.line(
		filtered_df,
		x='year',
		y=metric_col,
		title=f'{pretty} Over Time in {selected_country}'
	)
	return fig


if __name__ == "__main__":
	app.run(debug=True)