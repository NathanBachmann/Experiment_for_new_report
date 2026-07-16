# Import necessary libraries
import pandas as pd
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path

#template = jinja2.Template("Hello {{ name }}!")
#print(template.render(name="World"))

# Load the .tsv file into a DataFrame
file_path = "results/stats.tsv"  # Replace with the path to your .tsv file
df = pd.read_csv(file_path, sep='\t')

# Preview the first few rows of the DataFrame
df.head()

# Define the Jinja2 HTML template as a string
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Analysis Report</title>
    <style>
        table {
            width: auto;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px 16px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
            padding: 8px 24px;
        }
        tr:nth-child(even) { background-color: #f2f2f2; }
        tr:hover { background-color: #ddd; }
        .controls { margin: 10px 0; font-family: Arial, sans-serif; }
        .hidden { display: none; }
        button { padding: 5px 15px; margin: 0 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>DADA2 QC metrics</h1>
    <div class="controls">
        <label for="search">Search sample-id: </label>
        <input type="text" id="search" onkeyup="searchTable()" placeholder="Type to search...">
        &nbsp;&nbsp;
        <label for="entries">Show entries: </label>
        <select id="entries" onchange="updateTable()">
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
            <option value="100">100</option>
        </select>
        <span id="info"></span>
    </div>
    <table id="dataTable">
        <thead>
            <tr>
                {% for column in columns %}
                <th>{{ column }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for row in rows %}
            <tr>
                {% for value in row %}
                <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <div class="controls">
        <button onclick="prevPage()">Previous</button>
        <span id="pageInfo"></span>
        <button onclick="nextPage()">Next</button>
    </div>

    <script>
        var currentPage = 1;

        function updateTable() {
            currentPage = 1;
            renderPage();
        }

        function searchTable() {
            var query = document.getElementById('search').value.toLowerCase();
            var rows = document.querySelectorAll('#dataTable tbody tr');
            for (var i = 0; i < rows.length; i++) {
                var firstCell = rows[i].getElementsByTagName('td')[0];
                if (firstCell) {
                    var text = firstCell.textContent.toLowerCase();
                    rows[i].setAttribute('data-filtered', text.indexOf(query) === -1 ? 'true' : 'false');
                }
            }
            currentPage = 1;
            renderPage();
        }

        function renderPage() {
            var entries = parseInt(document.getElementById('entries').value);
            var allRows = document.querySelectorAll('#dataTable tbody tr');
            var visibleRows = [];
            for (var i = 0; i < allRows.length; i++) {
                if (allRows[i].getAttribute('data-filtered') === 'true') {
                    allRows[i].classList.add('hidden');
                } else {
                    visibleRows.push(allRows[i]);
                }
            }
            var totalRows = visibleRows.length;
            var totalPages = Math.ceil(totalRows / entries) || 1;
            var start = (currentPage - 1) * entries;
            var end = start + entries;

            for (var i = 0; i < visibleRows.length; i++) {
                if (i >= start && i < end) {
                    visibleRows[i].classList.remove('hidden');
                } else {
                    visibleRows[i].classList.add('hidden');
                }
            }

            document.getElementById('info').textContent =
                'Showing ' + (totalRows > 0 ? start + 1 : 0) + ' to ' + Math.min(end, totalRows) + ' of ' + totalRows + ' entries';
            document.getElementById('pageInfo').textContent =
                'Page ' + currentPage + ' of ' + totalPages;
        }

        function nextPage() {
            var entries = parseInt(document.getElementById('entries').value);
            var totalRows = document.querySelectorAll('#dataTable tbody tr').length;
            if (currentPage < Math.ceil(totalRows / entries)) {
                currentPage++;
                renderPage();
            }
        }

        function prevPage() {
            if (currentPage > 1) {
                currentPage--;
                renderPage();
            }
        }

        updateTable();
    </script>
</body>
</html>
"""

# Create a Jinja2 Template object from the HTML template string
template = Template(html_template)

# Render the template with the DataFrame data
html_report = template.render(
    columns=df.columns.tolist(),
    rows=df.values.tolist()
)

# Save the rendered HTML to a file
output_path = Path("report.html")
output_path.write_text(html_report)

