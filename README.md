# Shopify AI Analytics Assistant

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the server:
   uvicorn main:app --reload
4. Open browser:
   http://127.0.0.1:8000/docs

## Architecture
- FastAPI backend
- Shopify REST Admin API
- Simple rule-based intent detection

## Agent Flow
User → POST /ask → Intent detection → Shopify API → Response

## Sample API Request
POST /ask
{
  "store": "your-store-name",
  "question": "How many orders in last 30 days?"
}

## Sample Response
{
  "intent": "sales",
  "answer": "There are X orders in the last 30 days."
}

## Notes
- Shopify token is hardcoded for demo purposes.
