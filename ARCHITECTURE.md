# Zomato AI Restaurant Recommendation Service Architecture

## Project Overview
An AI-powered service that provides highly relevant restaurant recommendations using real-world Zomato data and Large Language Models (LLM).

## Technical Stack
- **Data**: Kaggle (`abhijitdahatonde/zomato-restaurants-dataset`)
- **Backend**: Python (Core Logic), Groq LLM
- **Frontend**: Next.js (React)
- **API**: Next.js Route Handlers (serving as Backend API)

## Phased Development Strategy

### Phase 1: Data Ingestion & Storage
- **Goal**: Fetch the Zomato dataset from Kaggle using `kagglehub`.
- **Components**: Data loader script using `KaggleDatasetAdapter`.
- **Outcome**: A clean, accessible dataset of restaurants saved as `zomato_data.csv`.

### Phase 2: User Preference & Filtering Engine
- **Goal**: Implement logic to filter restaurants based on user inputs.
- **Filters**: Price Range, Location (Place), Rating, Cuisine.
- **Outcome**: A subset of restaurants matching basic criteria.

### Phase 3: Groq LLM Integration (Intelligence)
- **Goal**: Use Groq LLM to analyze filtered results and generate natural language recommendations.
- **LLM**: Groq (using Llama-3-70b/8b).
- **Outcome**: Personalized, text-based recommendations that explain *why* a restaurant was chosen.

### Phase 4: Ranking & Optimization
- **Goal**: Rank recommendations based on weighted metrics (popularity, distance, sentiment).
- **Outcome**: The most relevant restaurants appear at the top.

### Phase 5: UI Implementation (Frontend)
- **Goal**: Build a premium React/Next.js interface.
- **Features**: 
    - Dynamic location dropdowns.
    - Interactive preference forms.
    - Clear recommendation cards with AI-generated descriptions.
- **Outcome**: A fully functional, user-friendly product.

## Data Flow
1. User enters preferences on UI.
2. Backend filters the Zomato Dataset.
3. Filtered list + Prompt sent to Groq LLM.
4. LLM returns structured/natural recommendations.
5. UI displays results.
