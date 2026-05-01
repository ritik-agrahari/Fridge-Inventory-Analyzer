# 🧊 Fridge Inventory Analyzer

## 🚀 Overview

The **Fridge Inventory Analyzer** is an AI-powered Streamlit web application that helps users intelligently manage their fridge contents. By simply uploading an image, the app detects food items, evaluates their freshness, and generates personalized recipe recommendations.

This project leverages **Google Generative AI** to provide smart insights, reduce food waste, and simplify meal planning.

---

## ✨ Key Features

* 📸 **Image-Based Detection** – Upload a fridge image to identify items automatically
* 🥦 **Categorization** – Classifies items into categories like vegetables, fruits, and beverages
* 🧪 **Freshness Analysis** – Detects condition (fresh, partially spoiled, rotten)
* 🍽️ **Recipe Generation** – Suggests recipes based on available ingredients
* 🔥 **Calorie Estimation** – Provides approximate calorie count per recipe
* 🎥 **YouTube Integration** – Suggests cooking tutorial links
* 🛒 **Smart Suggestions** – Lists missing ingredients required for recipes

---

## 🛠️ Tech Stack

* **Frontend & App Framework:** Streamlit
* **AI Model:** Google Generative AI
* **Image Processing:** Pillow (PIL)
* **Data Handling:** Pandas

---

## 📂 Project Structure

```
fridge-inventory-analyzer/
│── app.py
│── recipe_generator.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/fridge-inventory-analyzer.git
cd fridge-inventory-analyzer
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Set Up API Key

* Get your API key from Google Cloud Console
* Set it as an environment variable:

**Mac/Linux:**

```
export GOOGLE_API_KEY="your_api_key_here"
```

**Windows:**

```
set GOOGLE_API_KEY=your_api_key_here
```

---

## ▶️ Run the Application

```
streamlit run app.py
```

---

## 📸 How It Works

1. Upload an image of your fridge
2. AI analyzes and detects items
3. Items are categorized and freshness is evaluated
4. Recipes are generated based on available ingredients

---

## 🎯 Use Cases

* Reduce food wastage
* Smart meal planning
* Quick recipe discovery
* Kitchen inventory management

---

## 📌 Future Enhancements

* 🧠 Custom ML model for improved detection accuracy
* 📱 Mobile-friendly UI
* 🗂️ User login & fridge history tracking
* 🛍️ Direct grocery ordering integration

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Ritik Kumar Agrahari**

* B.Tech CSE (AI & ML)
* GATE Qualified (2025 & 2026)

---

## 🌟 Show Your Support

If you like this project, consider giving it a ⭐ on GitHub!
