# Fridge Inventory Analyzer

## Description

The Fridge Inventory Analyzer is a Streamlit web application designed to help users analyze the contents of their fridge by uploading an image. The application uses Google's Generative AI to detect and categorize items in the fridge, assess their condition (e.g., fresh, partially spoiled, or rotten), and generate personalized recipe suggestions based on the available ingredients. It also provides additional features such as estimating calorie counts for recipes and suggesting YouTube tutorials for cooking guidance.

## File Structure

- `app.py`: The main Streamlit application file that handles the user interface, image upload, and analysis of fridge contents using Google's Generative AI.
- `recipe_generator.py`: A module that generates recipe suggestions based on the detected fridge items. It uses Google's Generative AI to create detailed recipes, including step-by-step instructions, estimated calorie counts, and links to YouTube tutorials.

## Dependencies

The project requires the following Python libraries:

- `streamlit`: For building the web application interface.
- `google-generativeai`: For interacting with Google's Generative AI model.
- `pillow`: For handling and processing images (PIL library).
- `pandas`: For data manipulation and visualization.

These dependencies can be installed using pip:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. **Install Dependencies**:
   - Create a new directory for your project and navigate to it.
   - Install the required libraries by running:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up API Key**:
   - The application uses Google's Generative AI, which requires an API key.
   - To obtain an API key:
     - Go to the [Google Cloud Console](https://console.cloud.google.com/).
     - Create a new project or select an existing one.
     - Enable the Generative Language API.
     - Create an API key and copy it.
   - Set the API key as an environment variable:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
     On Windows:
     ```bash
     set GOOGLE_API_KEY=your_api_key_here
     ```

3. **Run the Application**:
   - Navigate to the project directory containing `app.py`.
   - Run the Streamlit app:
     ```bash
     streamlit run app.py
     ```

## Usage

1. **Upload an Image**:
   - Open the Streamlit app in your web browser (it will automatically open when you run `streamlit run app.py`).
   - Use the file uploader to select an image of your fridge.

2. **View Analysis**:
   - The app will process the uploaded image using Google's Generative AI.
   - It will display a list of detected items, categorized by type (e.g., Vegetables, Fruits, Beverages), along with their condition (e.g., fresh, spoiled) and quantity.

3. **Get Recipe Suggestions**:
   - Based on the detected items, the app will generate 2–3 simple recipes.
   - Each recipe includes:
     - A clear recipe name.
     - Step-by-step instructions.
     - Estimated calorie count per serving.
     - A YouTube search URL for a tutorial video.
   - The app will also list any additional ingredients you might need to buy.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or contributions, feel free to reach out to the developer.