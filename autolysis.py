import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import json
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")
PROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json"
}
def load_data(filename):
    try:
        # Try reading with utf-8 encoding first
        df = pd.read_csv(filename, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        # If utf-8 fails, try reading with ISO-8859-1 encoding
        print(f"UTF-8 decoding failed. Trying ISO-8859-1 encoding for {filename}.")
        try:
            df = pd.read_csv(filename, encoding='ISO-8859-1')
            return df
        except Exception as e:
            print(f"Error loading file with ISO-8859-1 encoding: {e}")
            return None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
def analyze_data(df):
    # Perform basic data analysis
    summary_stats = df.describe(include="all").to_dict()
    for col, stats in summary_stats.items():
        for stat, value in stats.items():
            if pd.isnull(value):
                summary_stats[col][stat] = None
    summary = {
        "columns": list(df.columns),
        "types": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": summary_stats,
        "correlation_matrix": df.corr(numeric_only=True).fillna(0).to_dict(),
    }
    return summary
def create_visualizations(df, output_dir):
    # Generate visualizations and save them as PNG files.
    os.makedirs(output_dir, exist_ok=True)
    # Histogram of up to 4 numeric columns
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if numeric_cols.empty:
        print("No numeric columns found for visualizations.")
    else:
        # Limit to 4 histograms
        hist_cols = numeric_cols[:4]
        for col in hist_cols:
            plt.figure()
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f"Distribution of {col}")
            plt.savefig(f"{output_dir}/{col}_histogram.png")
            plt.close()
    # Heatmap of correlations
    if not numeric_cols.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig(f"{output_dir}/correlation_heatmap.png")
        plt.close()
def query_llm(prompt):
    # Send a query to GPT-4o-Mini using AI Proxy
    try:
        # Construct the payload
        payload = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        # Make the POST request
        response = requests.post(PROXY_URL, headers=HEADERS, json=payload)
        # Handle the response
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return "Error querying LLM."
    except Exception as e:
        print(f"Error querying LLM: {e}")
        return "Error querying LLM."
def generate_markdown_story(df_summary, output_dir):
    # Generate README.md.
    prompt = (
        "You are a data scientist. Based on the following data analysis summary, "
        "write a narrative in Markdown format including insights and visualizations:" 
        f"\n\n{json.dumps(df_summary, indent=2)}"
    )
    narrative = query_llm(prompt)
    with open(f"{output_dir}/README.md", "w") as file:
        file.write(narrative)
def run_analysis(input_file):
    # Process the dataset
    try:
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}")
            return
        dataset_name = os.path.splitext(os.path.basename(input_file))[0]
        output_dir = dataset_name
        df = load_data(input_file)
        if df is None:
            return
        summary = analyze_data(df)
        create_visualizations(df, output_dir)
        generate_markdown_story(summary, output_dir)
        print(f"Analysis complete. Outputs saved in {output_dir}/")
    except Exception as e:
        print(f"An error occurred: {e}")
# Input the path to your dataset in the Jupyter Notebook
import glob

# Process all CSV files in the current directory
input_files = glob.glob("*.csv")
for input_file in input_files:
    print(f"Processing file: {input_file}")
    run_analysis(input_file)
