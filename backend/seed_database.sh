#!/bin/bash

# Seed database script
echo "🌱 Starting database seeding..."
echo ""

# Activate virtual environment and run seed script
source .venv/bin/activate
python seed_data.py

echo ""
echo "Done! Check your application to see the new data."
