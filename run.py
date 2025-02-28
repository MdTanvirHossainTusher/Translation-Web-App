#!/usr/bin/env python3
"""
Main entry point for the Healthcare Translation Web App.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8000)
    app.run()
