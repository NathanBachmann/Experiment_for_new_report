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
resources_dir = os.path.join(script_dir, "resources")

# Read logo
with open(os.path.join(resources_dir, "logo.txt")) as f:
    logo = f.read().strip()

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

dada_column_descriptions = {
    "sample-id": "Unique sample identifier",
    "input": "Number of raw input reads",
    "filtered": "Reads remaining after quality filtering",
    "percentage of input passed filter": "Percentage of input reads that passed quality filtering",
    "denoised": "Reads after DADA2 denoising",
    "non-chimeric": "Reads remaining after chimera removal",
    "percentage of input non-chimeric": "Percentage of input reads that are non-chimeric"
}

# Render the template with the DataFrame data
html_report = template.render(
    columns=df.columns.tolist(),
    rows=df.values.tolist(),
    logo=logo,
    parameters=parameters,
    dada_column_descriptions=dada_column_descriptions
)

# Save the rendered HTML to a file
output_path = Path("report.html")
output_path.write_text(html_report)

shutil.copy(os.path.join(script_dir, "templates", "understanding_the_analysis.html"), ".")