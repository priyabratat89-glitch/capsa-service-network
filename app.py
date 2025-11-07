from flask import Flask, render_template, request, jsonify
import pandas as pd
import re  # Import the regular expression module
import os
from datetime import datetime


app = Flask(__name__)

# Paths to your CSV files
#csv_file_path_1 = 'C:/Users/Priyabrata.T/Desktop/Python Project/RGH/HD-Data.csv'
csv_file_path_2 = 'C:/Users/Priyabrata.T/Desktop/Python Project/RGH/Pincode Serv/All-Data.csv'
csv_file_path_3 = 'C:/Users/Priyabrata.T/Desktop/Python Project/RGH/Pincode Serv/Serviceabilty.csv'

# Initialize DataFrames
#df1 = None
df2 = None
df3 = None

# Load CSV files into DataFrames
def load_data():
    global  df2, df3
    try:
       # df1 = pd.read_csv(csv_file_path_1, encoding='latin1')
        df2 = pd.read_csv(csv_file_path_2, encoding='latin1')
        df3 = pd.read_csv(csv_file_path_3, encoding='latin1')
       # df1['CustomerPin-code'] = df1['CustomerPin-code'].astype(str)
        df2['CustomerPin-code'] = df2['CustomerPin-code'].astype(str)
        df3['Pincode'] = df3['Pincode'].astype(str)
    except (FileNotFoundError, pd.errors.EmptyDataError) as e:
        print(f"Error loading CSV files: {e}")

# Call load_data to initialize dataframes
load_data()

# Function to retrieve data based on pincode
def retrieve_data(df, pincode):
    if df is not None:
        filtered_data = df[df['CustomerPin-code'].str.strip() == pincode.strip()]
        if filtered_data.empty:
            return None
        else:
            return filtered_data[['CustomerPin-code', 'ServingDC', 'State', 'GG-QWIK','GG-Delhivery','GG-Shadowfax','GG-Bluedart','GG-Min.','GG-Pref. Carr.',
                                  'HD-QWIK','HD-Delhivery','HD-Min.','HD-Pref. Carr.'
                                  
]]
    return None

def retrieve_data_csv(df, pincode):
    if df is not None:
        filtered_data = df[df['Pincode'].str.strip() == pincode.strip()]
        if filtered_data.empty:
            return None
        else:
            return filtered_data[['Pincode', 'QWIK GNG.','Del Serv.','Shadowfax Serv.','Bluedart Serv','Qwik HD.','Del HD.','City','State','Zone','GNG P1','HD P1']]
    return None

# Route to render HTML template with search form
@app.route('/')
def index():
    
    last_modified_dt = None
    if os.path.exists(csv_file_path_3):
        last_modified_time = os.path.getmtime(csv_file_path_3)
        last_modified_dt = datetime.fromtimestamp(last_modified_time).strftime('%Y-%m-%d %H:%M:%S')
    else:
        last_modified_dt = None  # Or you can set a message like "File not found"

    return render_template('index.html', last_modified_dt=last_modified_dt)

# Route to handle search request and return JSON response
@app.route('/search', methods=['POST'])
def search_pins():
    pincodes = request.form.get('pincodes')
    if pincodes:
        # Use regular expression to split by either commas or spaces
        pincodes = re.split(r'[,\s]+', pincodes.strip())
        
        results = []

        for pincode in pincodes:
            pincode = pincode.strip()  # Ensure no leading/trailing spaces
           # result_df1 = retrieve_data(df1, pincode)
            result_df2 = retrieve_data(df2, pincode)
            result_df3 = retrieve_data_csv(df3, pincode)

            result_text = f"Results for PIN Code {pincode}:<br><br>"
        
            if result_df3 is not None:
                result_text += "1. Status from Transport Serviceability:<br><br>" + result_df3.to_html(index=False) + "<br>"
            else:
                result_text += "Currently, we do not have service coverage for this pincode. We apologize for any inconvenience this may cause.!<br>"
                
           # if result_df1 is not None:
          #      result_text += "2. Data from HD Serviceability:<br><br>" + result_df1.to_html(index=False) + "<br>"
           # else:
             #   result_text += "2. No data found in HD Serviceability!<br>"

            if result_df2 is not None:
                result_text += "2. Data from GNG/HD Serviceability:<br><br>" + result_df2.to_html(index=False) + "<br>"
            else:
                result_text += "<br><br>"

            results.append(result_text)

        return jsonify(results=results)
    else:
        return jsonify(error='No PIN codes provided')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
