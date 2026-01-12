# AI Job Description Analyzer

An intelligent system to analyze job descriptions using NLP and Generative AI (GPT-2).

## Features
- **Automatic Skill Extraction**: Identifies technical and soft skills.
- **Experience Level Detection**: Classifies roles as Junior, Mid-level, or Senior.
- **AI-Powered Insights**: Generates professional summaries using GPT-2.
- **Analytics Dashboard**: Visualizes trends in analyzed job descriptions.
- **Analysis History**: Keeps track of all processed descriptions.

## Structure
- `app/`: Main Streamlit application.
- `preprocessing/`: Text cleaning and normalization.
- `analysis/`: Skill and experience level extraction logic.
- `generation/`: GPT-2 model integration and prompt engineering.
- `data/`: JSON storage for analysis history.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run app/streamlit_app.py
   ```

## Note
The first run will download the GPT-2 model (approx. 500MB). This may take a few minutes depending on your internet connection.
