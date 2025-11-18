# api/index.py
from mangum import Mangum
from app.main import app

handler = Mangum(app)

# Vercel expects a callable named `main` that takes a request
main = handler  # directly assign the Mangum handler
