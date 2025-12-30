import google.generativeai as genai

# Use the SAME key you're putting in gemini_snowflake.py
API_KEY = "AIzaSyBxnoYnEcWXC1fsScFBQyqmwRxsRMyphPQ"

genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content("Hello")
    print("✅ API WORKS with gemini-2.5-flash!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ API FAILED")
    print(f"Error: {str(e)}")