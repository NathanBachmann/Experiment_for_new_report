# Import necessary libraries
import pandas as pd
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
import os
import shutil
import configparser

#functions
def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


#Set variables
script_dir = get_script_dir()
resources_dir = os.path.join(script_dir, "resources")

config = configparser.ConfigParser()
config.read(os.path.join(script_dir, "help_descriptions.ini"))

# Read logo
with open(os.path.join(resources_dir, "logo.txt")) as f:
    logo = f.read().strip()

# Read project Information
with open("project_info.txt") as f:
    project_info = f.read()

# Read in analysis summary
with open("analysis_summary.txt") as f:
    analysis_summary = [line.strip() for line in f.readlines()]

# Read parameters file
with open("parameters.txt") as f:
    parameters = f.read()

# Read software versions
with open("software_versions.txt") as f:
    software_versions = f.read()

# Load the stats.tsv file into a DataFrame
file_path = "results/stats.tsv"  # Replace with the path to your .tsv file
df = pd.read_csv(file_path, sep='\t')

# Preview the first few rows of the DataFrame
df.head()

# Load template
env = Environment(loader=FileSystemLoader(os.path.join(script_dir, "templates")))
template = env.get_template("main_report.html")

dada_column_descriptions = dict(config["dada_column_descriptions"])

# Render the template with the DataFrame data
html_report = template.render(
    columns=df.columns.tolist(),
    rows=df.values.tolist(),
    logo=logo,
    project_info=project_info,
    analysis_summary=analysis_summary,
    parameters=parameters,
    dada_column_descriptions=dada_column_descriptions,
    software_versions=software_versions
)

# Save the rendered HTML to a file
output_path = Path("report.html")
output_path.write_text(html_report)

shutil.copy(os.path.join(script_dir, "templates", "understanding_the_analysis.html"), ".")