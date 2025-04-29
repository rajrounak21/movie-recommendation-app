# 🎬 Movie Recommendation System

A content-based movie recommendation web app built using Python, Streamlit, and the TMDb API. The system recommends similar movies based on selected titles using Natural Language Processing and cosine similarity.

## 🚀 Features

- Recommends top 5 similar movies based on user selection
- Uses TF-based vectorization and cosine similarity for comparison
- Displays movie posters using the TMDb API
- Clean and responsive UI built with Streamlit

## 🧠 How It Works

1. **Data Cleaning & Preprocessing**  
   - Merged TMDB movie and credits datasets
   - Extracted important metadata: genres, cast, crew, keywords, and overview
   - Preprocessed text (tokenization, stemming, and normalization)

2. **Feature Engineering**  
   - Created a `tags` field combining all relevant metadata
   - Vectorized tags using `CountVectorizer`
   - Computed cosine similarity to compare movies

3. **Recommendation Logic**  
   - For a selected movie, fetches the top 5 most similar ones
   - Retrieves movie posters via TMDb API

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Libraries:** Pandas, NumPy, scikit-learn, joblib, requests, NLTK
- **Dataset link:**((http://kaggle.com/datasets/tmdb/tmdb-movie-metadata))

## 🗂️ Project Structure

```plaintext
├── recommend.py                 # Streamlit app
├── project.py # Data cleaning and model generation
├── movie.joblib          # Preprocessed movie data
├── similarity.joblib     # Cosine similarity matrix
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


▶️ Getting Started
1. Clone the Repository
git clone https://github.com/rajrounak21/movie-recommendation-app.git
cd movie-recommendation-app
2. Install Dependencies
pip install -r requirements.txt
3. Run the App
streamlit run app.py
