# 🎯 PitchSnitch

A dark-themed Streamlit application powered by Claude that transforms raw hackathon ideas into winning strategies and actionable plans.

## Features

- **Comprehensive Analysis**: Evaluates ideas across 8 key dimensions
- **Executive Summary**: Get a quick assessment of your idea's viability
- **Detailed Scores**: Problem clarity, user value, market size, technical feasibility, and more
- **Implementation Plan**: Step-by-step roadmap tailored to your constraints
- **Risk Assessment**: Identify potential challenges before you start building
- **Tech Stack Recommendations**: LLM-generated technology suggestions
- **48-Hour Checklist**: Actionable tasks broken down for hackathon timeframes
- **5-Slide Pitch Deck**: Ready-to-use presentation content for judges

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PitchSnitch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

4. **Run PitchSnitch**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Describe Your Idea**: Enter your hackathon concept, target users, and goals
2. **Set Constraints**: Specify team size and time available
3. **Get Analysis**: Claude evaluates your idea across 8 dimensions
4. **Review Results**: See scores, implementation plan, risk flags, and tech recommendations
5. **Build Your Pitch**: Use the generated 5-slide presentation content for judges

## Evaluation Dimensions

The coach analyzes your idea across these 8 key areas:

1. **Problem Clarity** (0-5) - How well-defined is the problem you're solving?
2. **User Value** (0-5) - How valuable is your solution to target users?
3. **Market Size & Urgency** (0-5) - Is there a significant, pressing market need?
4. **Differentiation/Moat** (0-5) - What makes your approach unique?
5. **Technical Feasibility** (0-5) - Can this be built in 48 hours?
6. **Scalability Path** (0-5) - How easily can this grow beyond the hackathon?
7. **Data Dependencies** (0-5) - How complex are your data requirements?
8. **Risks & Compliance** (0-5) - What regulatory or technical risks exist?

## 5-Slide Pitch Deck

Generated presentation content includes:
1. **Problem Statement** - Clear pain points and target audience
2. **Solution Overview** - Key features and unique value proposition  
3. **Technical Approach** - Implementation details and tech stack
4. **Market Opportunity** - Size, validation, and business potential
5. **Business Model** - Revenue strategy and growth plan

## Requirements

- Python 3.8+
- Anthropic API key
- Streamlit 1.28+

## Author

**Geetanshi Goel**
- GitHub: [@geetanshi](https://github.com/geetanshi0205)
- LinkedIn: [Geetanshi Goel](https://www.linkedin.com/in/geetanshi-goel-49ba5832b/)

---

## License

MIT License