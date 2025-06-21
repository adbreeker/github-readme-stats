"""
Test script to verify environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test if PAT is loaded
pat = os.getenv('PAT_1')
cache_seconds = os.getenv('CACHE_SECONDS')

print("Environment Variables Test:")
print("=" * 40)
print(f"PAT_1: {'✓ Loaded' if pat else '✗ Missing'}")
if pat:
    print(f"PAT_1 value: {pat[:10]}...{pat[-10:] if len(pat) > 20 else pat}")

print(f"CACHE_SECONDS: {cache_seconds}")
print(f"PORT: {os.getenv('PORT', '5000')}")
print(f"FLASK_ENV: {os.getenv('FLASK_ENV', 'not set')}")

if pat:
    print("\n✅ Ready to run the Flask application!")
    print("Run: python app.py")
else:
    print("\n❌ PAT_1 is missing. Please check your .env file.")
