import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# Load your final dataframe (ensure it is in the same directory or provide the correct path)
data = pd.read_excel('./utilities/sorted_first.xlsx')

# This function checks for the presence of genes associated with a given bigg_id
def find_locations_for_bigg_id(bigg_id):
    # Filter the dataframe by bigg_id
    filtered_df = data[data['bigg_id'] == bigg_id]
    
    # If no matching bigg_id found
    if filtered_df.empty:
        return None
    
    # Get all location columns, excluding the 'bigg_id' and 'gene_id' columns
    location_columns = [col for col in data.columns if col not in ['bigg_id', 'gene_id', 'others', 'pathway', 'reaction_name', 'reaction_string', 'gene_id_list']]
    
    # Store the locations where the genes are found
    found_locations = {}
    
    for col in location_columns:
        # Check if the location column has any gene listed for this bigg_id
        genes = filtered_df[col].dropna().tolist()
        if genes:
            found_locations[col] = genes
    
    return found_locations

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/search', methods=['POST'])
def search():
    bigg_id = request.form['bigg_id']
    
    # Find locations for the given bigg_id
    locations = find_locations_for_bigg_id(bigg_id)
    
    # If no locations are found, return a message
    if locations is None:
        return render_template('index.html', bigg_id=bigg_id, message="No results found for the given bigg_id.")
    
    # Return the results to the user
    return render_template('index.html', bigg_id=bigg_id, locations=locations)

if __name__ == '__main__':
    app.run(debug=True)
