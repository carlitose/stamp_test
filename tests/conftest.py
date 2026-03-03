import os
import sys

# Add src/lambda to path for all tests
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "lambda"))

# Set consistent env vars before any module imports Config
os.environ["SENDER_EMAIL"] = "sender@example.com"
os.environ["AWS_REGION"] = "eu-south-1"
