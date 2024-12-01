import pandas as pd
import plotly.express as px
from flask import Flask, render_template

# Initialize the Flask app
app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Load the CSV data
        data = pd.read_csv("malaria/malaria_indicators_ssd.csv")

        # Drop irrelevant columns
        columns_to_drop = ['GHO (CODE)', 'GHO (DISPLAY)', 'GHO (URL)', 'STARTYEAR', 'ENDYEAR', 
                           'REGION (CODE)', 'REGION (DISPLAY)', 'COUNTRY (CODE)', 'COUNTRY (DISPLAY)', 
                           'DIMENSION (TYPE)', 'DIMENSION (CODE)', 'DIMENSION (NAME)', 'Low', 'High']
        data_clean = data.drop(columns=columns_to_drop)

        # Rename columns for simplicity
        data_clean.rename(columns={'YEAR (DISPLAY)': 'Year', 'Value': 'Cases'}, inplace=True)

        # Clean up the 'Cases' column (remove commas and spaces, convert to numeric)
        data_clean['Cases'] = data_clean['Cases'].replace({',': '', ' ': ''}, regex=True)
        data_clean['Cases'] = pd.to_numeric(data_clean['Cases'], errors='coerce')  # Convert to numeric, coercing errors

        # Handle missing values (drop rows with missing 'Cases' values)
        data_clean.dropna(subset=['Cases'], inplace=True)

        # Print the cleaned data to the console for debugging
        print(data_clean.head())

        # Create the plot
        fig = px.line(data_clean, x='Year', y='Cases', title="Malaria Cases Over Time")
        
        # Convert the plot to HTML
        graph_html = fig.to_html(full_html=False)

        return render_template('index.html', graph_html=graph_html)

    except Exception as e:
        print(e)  # Print the error for debugging
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
