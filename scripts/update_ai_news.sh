#!/bin/bash
# AI News Auto-Update Script for Cicadas
# This script updates AI news data and pushes to GitHub

# Set working directory
cd /Users/duoduodaye/cicidas

# Log file
LOG_FILE="scripts/ai_news_update.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting AI news update..." >> "$LOG_FILE"

# Run news fetcher
cd scripts
python3 ai_news_fetcher.py >> "../$LOG_FILE" 2>&1

# Check if new data was generated
if [ -f "ai_news_data.js" ]; then
    echo "[$DATE] News data generated successfully" >> "../$LOG_FILE"
    
    # Copy to main directory
    cp ai_news_data.js ../ 
    cp ai_news_data.json ../
    
    cd ..
    
    # Check if there are changes
    if git diff --quiet ai_news_data.js ai_news_data.json; then
        echo "[$DATE] No changes in news data, skipping update" >> "$LOG_FILE"
    else
        echo "[$DATE] Changes detected, updating repository..." >> "$LOG_FILE"
        
        # Add and commit changes
        git add ai_news_data.js ai_news_data.json
        
        # Create commit message with stats
        STATS=$(python3 -c "
import json
with open('ai_news_data.json', 'r') as f:
    data = json.load(f)
print(f\"Update AI news: {data['totalArticles']} articles, {data['featuredCount']} featured\")
")
        
        git commit -m "$STATS

🤖 Automated news update - $(date '+%Y-%m-%d %H:%M')

Sources: $(python3 -c "
import json
with open('ai_news_data.json', 'r') as f:
    data = json.load(f)
print(', '.join(data['sources']))
")

Co-Authored-By: AI News Bot <noreply@cicidas.org>"
        
        # Push to GitHub
        if git push origin main; then
            echo "[$DATE] Successfully pushed to GitHub" >> "$LOG_FILE"
        else
            echo "[$DATE] Failed to push to GitHub" >> "$LOG_FILE"
        fi
    fi
else
    echo "[$DATE] Failed to generate news data" >> "$LOG_FILE"
fi

echo "[$DATE] AI news update completed" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"