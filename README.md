# Zomato AI Recommendation Service 🍴🤖

A premium, AI-powered restaurant discovery platform for Bangalore. This project leverages real-time Zomato data and LLM-powered expert insights to help users find the perfect dining experience.

## ✨ Key Features
- **AI Expert Concierge**: Personalized restaurant breakdowns using Llama 3 (via Groq Cloud).
- **Phased Discovery**: Multi-stage filtering (Location, Cuisine, Budget, Rating).
- **Secure Authentication**: Integrated **Real Firebase Google Auth** bridge for secure user sessions.
- **Premium UI/UX**: Centered layouts, universal theme switching (Dark/Light), and responsive photography.
- **Data Transparency**: Interactive "See How" panel explaining the filtering and ranking logic.

## 🏗️ Project Architecture
The project follows a phased development approach:
- **Phase 1**: Data ingestion and cleaning from Kaggle.
- **Phase 2**: Core recommendation and filtering logic.
- **Phase 3**: LLM (Groq) integration for natural language insights.
- **Phase 4**: Ranking algorithms and final score normalization.
- **Frontend**: High-performance Streamlit app + Complementary Next.js frontend (`zomato-ai-ui`).

## 🛠️ Tech Stack
- **Backend/Logic**: Python 3.x
- **Frontend 1**: Streamlit (with Custom CSS Variables)
- **Frontend 2**: Next.js (Modern Tailwind UI)
- **AI Engine**: Groq (Llama-3-70b/8b)
- **Auth**: Firebase (Google OAuth SDK)
- **Data**: Pandas / Kaggle Zomato Dataset

## 🚀 Getting Started

### 1. Requirements
Ensure you have the following installed:
- Python 3.8+
- Node.js (for Next.js frontend)

### 2. Setup Environment
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Apps

**Run Streamlit (Recommended):**
```bash
streamlit run streamlit_app.py
```

**Run Next.js Frontend:**
```bash
cd zomato-ai-ui
npm install
npm run dev
```

## 📁 Repository Structure
- `streamlit_app.py`: Main interactive experience.
- `phase[1-4]/`: Evolutionary development stages and module tests.
- `zomato-ai-ui/`: Next.js frontend project.
- `ARCHITECTURE.md`: Detailed technical breakdown of the engine.
- `zomato_data.csv`: Local reference dataset.

---
*Built with ❤️ for Foodies in Bangalore.*
