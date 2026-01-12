import os
import glob
import requests
import json
import argparse

# Configuration
INPUT_DIR = "../outputs/aggregates/"
OUTPUT_FILE = "../outputs/llm_analysis_report.md"

# You can swap this URL for OpenAI/Anthropic/Google API endpoints
# This example assumes a generic OpenAI-compatible completion endpoint
API_URL = "https://api.openai.com/v1/chat/completions"

def read_aggregates():
    """Reads all CSVs in the aggregates folder and concatenates them."""
    context = ""
    files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))
    if not files:
        print(f"[!] No CSV files found in {INPUT_DIR}")
        return None

    for f in files:
        filename = os.path.basename(f)
        context += f"\n\n--- FILE: {filename} ---\n"
        with open(f, 'r', encoding='utf-8') as fh:
            # Read first 50 lines to avoid token limits if files are huge (aggregates shouldn't be)
            content = fh.read(4000) 
            context += content
    return context

def query_llm(api_key, context, goal):
    """Sends the context to the LLM."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    prompt = f"""
    You are a Senior Security Data Analyst.
    I am providing you with AGGREGATE statistics from a historical partial database dump (BreachForums MyBB users).
    
    GOAL: {goal}
    
    DATA (CSVs):
    {context}
    
    INSTRUCTIONS:
    1. Analyze the growth trends (registration dates).
    2. Analyze the security posture (password algos, 2FA adoption).
    3. Analyze the community demographics (languages, timezones).
    4. Highlight any anomalies (e.g., weird timezones or rapid growth spikes).
    5. Output the report in Markdown format.
    """

    data = {
        "model": "gpt-4o", # Or gpt-4-turbo, etc.
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error querying API: {e} - Response: {response.text if response else ''}"

def main():
    parser = argparse.ArgumentParser(description="Generate AI analysis from aggregate CSVs")
    parser.add_argument("--key", required=True, help="Your LLM API Key (OpenAI/etc)")
    parser.add_argument("--goal", default="Generate a security finding summary for the README", help="Analysis Goal")
    args = parser.parse_args()

    print("[*] Reading aggregate data...")
    context = read_aggregates()
    if not context:
        return

    print("[*] Querying LLM (this may take a moment)...")
    report = query_llm(args.key, context, args.goal)

    print(f"[*] Saving report to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print("[+] Done.")

if __name__ == "__main__":
    main()
