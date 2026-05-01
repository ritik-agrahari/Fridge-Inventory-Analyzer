
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import json
import re
import os
import pandas as pd
import recipe_generator

# Configure Streamlit page
st.set_page_config(page_title="Fridge Inventory Analyzer", page_icon="🧊", layout="wide")

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY", "Google API KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.0-flash")

# Sidebar for developer details
with st.sidebar:
    st.header("Developer Details")
    st.markdown("**Name**: Ritik Kumar Agrahari")
    st.markdown("**Email**: [ritik131201@gmail.com](mailto:ritik131201@gmail.com)")
    st.markdown("**LinkedIn**: [Ritik Agrahari](https://www.linkedin.com/in/ritik-agrahari)")
    st.markdown("---")
    st.info("Built to get rid of daily question----> Aaj khane main kya banana hai??")

# Streamlit app layout
st.title("🧊 Fridge Inventory Analyzer")
st.markdown("Upload an image of your fridge to get a detailed analysis of its contents and personalized recipe suggestions with step-by-step instructions, calorie estimates, and video tutorials!")

# Image upload
uploaded_file = st.file_uploader("Choose a fridge image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    st.image(uploaded_file, caption="Uploaded Fridge Image", use_column_width=True)

    # Load image
    try:
        image = Image.open(uploaded_file)
    except Exception as e:
        st.error(f"Error loading image: {e}")
        st.stop()

    # Enhanced prompt for detailed object detection
    prompt = """
Act as an expert in fridge inventory analysis with a focus on precision and detail. Analyze the provided fridge image and detect all objects with high accuracy. Provide a comprehensive JSON response with the following structure for each detected object: 
{
  "label": "item_name",
  "category": "category_name",
  "condition": "condition_description",
  "quantity": estimated_quantity,
  "size": "approximate_size",
  "confidence": confidence_score
}
Follow these instructions:

1. **Object Detection**:
   - Detect every visible item in the fridge, including food, containers, and other objects, even if partially occluded or small.
   - Identify specific items (e.g., "red apple" instead of "apple", "half-empty milk jug" instead of "milk").
   - Estimate the quantity of each item as a string (e.g., "2", "many", "approx. 500ml remaining").
   - Estimate the approximate size (e.g., "small", "medium", "large", or specific measurements like "approx. 200ml").

2. **Categorization**:
   - Assign each item to one of the following categories:
     - **Vegetables**: Items like peppers, carrots, broccoli, lettuce, etc.
     - **Fruits**: Items like apples, oranges, kiwis, bananas, etc.
     - **Beverages**: Items like milk, juice, soda, water bottles, etc.
     - **Spices/Condiments**: Items like spice jars, sauces, ketchup, mustard, etc.
     - **Other**: Items that don’t fit the above (e.g., shelves, containers, cheese, meat, etc.).
     - **Spoilage**: Stains, spills, or spoiled items not suitable for consumption.

3. **Condition Assessment**:
   - For each food item, assess its condition based on visual cues:
     - "fresh": Appears vibrant, no discoloration or damage.
     - "partially spoiled": Minor discoloration, wilting, or bruising (e.g., "slightly wilted lettuce").
     - "rotten": Significant spoilage signs like mold, rot, or foul discoloration (e.g., "rotten with mold spots").
     - For containers, note if they are "full", "half-empty", or "nearly empty".
     - For stains/spills, use "label": "stain", "category": "Spoilage", "condition": "visible spill" with a description (e.g., "sticky residue on shelf").
   - Provide specific observations (e.g., "brown spots on banana", "mold on cheese").

4. **Confidence Score**:
   - Assign a confidence score (0.0 to 1.0) for each detection based on clarity and certainty of identification (e.g., 0.9 for clear items, 0.6 for partially occluded items).

5. **Output Format**:
   - Return a JSON array of objects, e.g., [{"label": "red apple", "category": "Fruits", "condition": "fresh", "quantity": "2", "size": "medium", "confidence": 0.9}, ...].

6. **Additional Notes**:
   - If an item’s category is ambiguous, make an educated guess and note uncertainty in "condition" (e.g., "possibly cheese, unclear due to occlusion").
   - Exclude non-items like fridge walls or doors unless they have stains/spills.
   - Prioritize accuracy by cross-referencing visual cues (color, shape, packaging) with common fridge items.
"""
    # Generate content
    with st.spinner("Analyzing fridge contents..."):
        try:
            response = model.generate_content([prompt, image])
            json_str = re.search(r'\[.*\]', response.text, re.DOTALL)
            if json_str is None:
                st.error("No valid JSON array found in response")
                st.write("Raw response:", response.text)
                st.stop()
            detections = json.loads(json_str.group(0))
        except (ValueError, json.JSONDecodeError) as e:
            st.error(f"Error parsing response: {e}")
            st.write("Raw response:", response.text)
            st.stop()

    # Organize items by category
    categories = {"Vegetables": [], "Fruits": [], "Beverages": [], "Spices/Condiments": [], "Other": [], "Spoilage": []}
    for detection in detections:
        category = detection.get("category", "Other")
        if category in categories:
            categories[category].append(detection)
        else:
            categories["Other"].append(detection)

    # Display items by category
    st.header("Fridge Contents Analysis")
    for category, items in categories.items():
        if items:
            st.subheader(category)
            # Create a DataFrame for detailed visualization, ensuring Quantity is string
            data = [
                {
                    "Label": item["label"],
                    "Condition": item["condition"],
                    "Quantity": str(item.get("quantity", "N/A")),  # Convert to string
                    "Size": item.get("size", "N/A"),
                    "Confidence": f"{item.get('confidence', 0.0):.2f}"
                }
                for item in items
            ]
            # Use pandas DataFrame with explicit string type for Quantity
            df = pd.DataFrame(data, columns=["Label", "Condition", "Quantity", "Size", "Confidence"])
            df["Quantity"] = df["Quantity"].astype(str)  # Ensure Quantity is string
            st.table(df)

    # Generate and display recipes
    with st.spinner("Generating recipe suggestions..."):
        recipes, to_buy = recipe_generator.generate_recipes(detections)

    st.header("Recipe Suggestions")
    for i, recipe in enumerate(recipes, 1):
        with st.expander(f"Recipe {i}: {recipe.get('name', 'Untitled Recipe')}"):
            st.markdown(f"**Estimated kcal per serving**: {recipe.get('kcal_per_serving', 'N/A')}")
            st.markdown("**Steps**:")
            steps = recipe.get("steps", [])
            if steps:
                for step_num, step in enumerate(steps, 1):
                    st.markdown(f"{step_num}. {step}")
            else:
                st.markdown("No steps provided.")
            youtube_url = recipe.get("youtube_url", None)
            if youtube_url:
                st.markdown(f"[Watch Tutorial on YouTube]({youtube_url})")
            else:
                st.warning("No YouTube tutorial available for this recipe.")

    if to_buy:
        st.header("Items to Buy")
        for item in to_buy:
            st.write(f"- {item}")
else:
    st.info("Please upload an image to start the analysis.")