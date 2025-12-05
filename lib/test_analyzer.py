import openai
import os
import subprocess
import json

# Set your OpenAI API key from environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_git_diff():
    # Get the diff of the latest commit
    try:
        # Use subprocess to run git command
        diff = subprocess.check_output(['git', 'diff', 'HEAD~1', 'HEAD'], encoding='utf-8')
        return diff
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e}")
        return ""

def get_test_recommendations(diff):
    if not diff:
        return "No code changes detected, no extra tests needed."

    prompt = f"""
    Analyze the following Git diff and recommend a specific number of test cases or a list of existing test files/functions that should be run to verify these changes. 
    Focus on impact analysis. 
    The output should be a JSON object with a 'test_cases' key, containing an array of strings (test names/descriptions), and a 'count' key (integer).

    Git Diff:
    {diff}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", # Use an appropriate model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        recommendation_text = response.choices[0].message.content.strip()
        # Attempt to parse the JSON response
        return recommendation_text
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return json.dumps({"test_cases": ["Default test suite run due to API error"], "count": 1})


if __name__ == "__main__":
    diff_text = get_git_diff()
    recommendation = get_test_recommendations(diff_text)
    # Print the JSON output to standard output for Jenkins to capture
    print(recommendation)
