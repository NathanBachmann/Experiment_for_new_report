# Import necessary libraries
import pandas as pd
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
import os
import shutil

#functions
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


#Set variables
script_dir = get_script_dir()

# Read parameters file
with open("parameters.txt") as f:
    parameters = f.read()

# Load the stats.tsv file into a DataFrame
file_path = "results/stats.tsv"  # Replace with the path to your .tsv file
df = pd.read_csv(file_path, sep='\t')

# Preview the first few rows of the DataFrame
df.head()

# Load template
env = Environment(loader=FileSystemLoader(os.path.join(script_dir, "templates")))
template = env.get_template("main_report.html")

# Render the template with the DataFrame data
html_report = template.render(
    columns=df.columns.tolist(),
    rows=df.values.tolist(),
    parameters=parameters
)

# Save the rendered HTML to a file
output_path = Path("report.html")
output_path.write_text(html_report)

shutil.copy(os.path.join(script_dir, "templates", "understanding_the_analysis.html"), ".")