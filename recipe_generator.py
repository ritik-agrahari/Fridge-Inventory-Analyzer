
import google.generativeai as genai
import os
import re
import json
import urllib.parse

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "AIzaSyCxK_S56Rr4GPajz-OljM9HssxEj6ht7ww"))

# Load Gemini model (flash for faster response)
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_recipes(detections):
    """
    Generates detailed recipes based on fridge items using Gemini AI.
    Returns a list of recipes with step-by-step instructions, estimated kcal per serving, YouTube links, and a list of additional ingredients to buy.
    """
    if not detections:
        return [{"name": "No ingredients detected", "steps": ["No ingredients detected."], "kcal_per_serving": 0, "youtube_url": None}], []

    # Create a text input for Gemini
    prompt = """
You are a professional recipe suggestion assistant with expertise in nutrition.
Given the list of available ingredients with detailed attributes, suggest 2–3 simple recipes that can be made with them.
For each recipe, provide:
- A clear recipe name.
- A list of step-by-step instructions, ensuring clarity and specificity (e.g., include quantities from the ingredient list, avoid spoiled items).
- An estimated kcal per serving, calculated based on the ingredients used (use standard nutritional data, e.g., apple ~52 kcal/100g, milk ~50 kcal/100ml).
- A YouTube search URL for a tutorial video.
Also, mention if any common ingredients are missing and should be bought from the market.

Respond only in JSON format like this:
{
  "recipes": [
    {
      "name": "recipe_name",
      "steps": ["step 1", "step 2", ...],
      "kcal_per_serving": estimated_kcal,
      "youtube_url": "https://www.youtube.com/results?search_query=recipe_name+tutorial"
    },
    ...
  ],
  "to_buy": ["item1", "item2"]
}

Here is the list of ingredients with their attributes:
"""
    for item in detections:
        label = item["label"]
        condition = item["condition"]
        quantity = item.get("quantity", "N/A")
        size = item.get("size", "N/A")
        confidence = item.get("confidence", 0.0)
        prompt += f"- {label} (Condition: {condition}, Quantity: {quantity}, Size: {size}, Confidence: {confidence:.2f})\n"

    # Generate response
    try:
        response = model.generate_content(prompt)
        json_data_match = re.search(r'{.*}', response.text, re.DOTALL)
        if json_data_match:
            data = json.loads(json_data_match.group())
            recipes = data.get("recipes", [])
            to_buy = data.get("to_buy", [])
            # Ensure YouTube URLs are properly formatted
            for recipe in recipes:
                if "youtube_url" not in recipe or not recipe["youtube_url"]:
                    recipe_name = recipe.get("name", "recipe")
                    query = urllib.parse.quote(f"{recipe_name} tutorial")
                    recipe["youtube_url"] = f"https://www.youtube.com/results?search_query={query}"
            return recipes, to_buy
        else:
            raise ValueError("No JSON found in Gemini response.")
    except Exception as e:
        return [{"name": "Error", "steps": [f"Error generating recipes: {str(e)}"], "kcal_per_serving": 0, "youtube_url": None}], []