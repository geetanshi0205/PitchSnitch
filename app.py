import streamlit as st
import os
from dotenv import load_dotenv
from anthropic import Anthropic
from dataclasses import dataclass
from typing import List, Dict, Any
import json

load_dotenv()

@dataclass
class IdeaInput:
    idea: str
    target_users: str
    time_constraint: int
    team_size: int
    goals: str

@dataclass
class EvaluationScore:
    dimension: str
    score: int
    reasoning: str

@dataclass
class AnalysisResult:
    executive_summary: str
    scores: List[EvaluationScore]
    detailed_plan: str
    risk_flags: List[str]
    build_checklist: List[str]
    tech_stack: Dict[str, List[str]]
    pitch_deck: Dict[str, str]
    overall_score: float

class HackathonIdeaCoach:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.evaluation_dimensions = [
            "Problem clarity",
            "User value",
            "Market size & urgency",
            "Differentiation/moat",
            "Technical feasibility in 48 hours",
            "Scalability path",
            "Data dependencies",
            "Risks & compliance"
        ]
    
    def analyze_idea(self, idea_input: IdeaInput) -> AnalysisResult:
        prompt = self._build_analysis_prompt(idea_input)
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = self._parse_claude_response(response.content[0].text)
            return result
            
        except Exception as e:
            st.error(f"Error analyzing idea: {str(e)}")
            return self._create_empty_result()
    
    def _build_analysis_prompt(self, idea_input: IdeaInput) -> str:
        return f"""
You are an expert hackathon mentor analyzing a team's idea. Provide a structured analysis.

IDEA: {idea_input.idea}
TARGET USERS: {idea_input.target_users}
TIME CONSTRAINT: {idea_input.time_constraint} hours
TEAM SIZE: {idea_input.team_size} people
GOALS: {idea_input.goals}

Analyze this idea across these 8 dimensions (score 0-5 each):
1. Problem clarity (0-5)
2. User value (0-5)
3. Market size & urgency (0-5)
4. Differentiation/moat (0-5)
5. Technical feasibility in 48 hours (0-5)
6. Scalability path (0-5)
7. Data dependencies (0-5)
8. Risks & compliance (0-5)

Also prepare detailed content for a 5-slide pitch deck presentation. Each slide should have substantial, well-developed content that teams can use directly in their presentations. Make the content comprehensive and compelling for hackathon judges.

Please respond in this exact JSON format:
{{
    "executive_summary": "2-3 sentence high-level assessment",
    "scores": [
        {{"dimension": "Problem clarity", "score": 4, "reasoning": "Clear explanation"}},
        // ... continue for all 8 dimensions
    ],
    "detailed_plan": "Structured implementation plan with key milestones",
    "risk_flags": ["Risk 1", "Risk 2", "Risk 3"],
    "build_checklist": ["Task 1", "Task 2", "Task 3", "..."],
    "tech_stack": {{
        "Frontend": ["React", "TypeScript", "Tailwind CSS"],
        "Backend": ["Node.js", "Express", "PostgreSQL"],
        "AI/ML": ["OpenAI API", "Langchain"],
        "Infrastructure": ["Vercel", "Supabase"],
        "Tools": ["Git", "VS Code", "Figma"]
    }},
    "pitch_deck": {{
        "slide1_problem": "Detailed problem statement (3-4 paragraphs): Start with a compelling hook, describe the pain points in detail, quantify the problem with statistics if possible, clearly define the target audience and their struggles, and explain why this problem matters now. Include emotional impact and urgency.",
        "slide2_solution": "Comprehensive solution description (3-4 paragraphs): Clearly explain your solution approach, detail 3-4 key features with specific benefits, highlight what makes your solution unique compared to alternatives, describe the user experience and journey, and explain the core value proposition with concrete examples.",
        "slide3_techstack": "Detailed technical approach (3-4 paragraphs): Explain your technology choices and why they're optimal for this problem, describe the system architecture and key components, highlight any innovative technical approaches or algorithms, discuss scalability and performance considerations, and mention specific frameworks, APIs, or tools that make your solution powerful.",
        "slide4_market": "Comprehensive market analysis (3-4 paragraphs): Provide market size data with specific numbers (TAM, SAM, SOM if possible), identify target customer segments with demographics, analyze competitors and your competitive advantages, discuss market timing and trends that favor your solution, and include validation evidence like user interviews or early traction.",
        "slide5_business_model": "Detailed business strategy (3-4 paragraphs): Clearly explain your revenue model with specific pricing strategy, describe customer acquisition channels and growth tactics, outline key partnerships and distribution strategies, provide financial projections or unit economics, discuss scalability plans and expansion opportunities, and explain your competitive moat and defensibility."
    }}
}}
"""
    
    def _parse_claude_response(self, response: str) -> AnalysisResult:
        try:
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            data = json.loads(json_str)
            
            scores = [EvaluationScore(**score) for score in data['scores']]
            overall_score = sum(score.score for score in scores) / len(scores)
            
            return AnalysisResult(
                executive_summary=data['executive_summary'],
                scores=scores,
                detailed_plan=data['detailed_plan'],
                risk_flags=data['risk_flags'],
                build_checklist=data['build_checklist'],
                tech_stack=data.get('tech_stack', {}),
                pitch_deck=data.get('pitch_deck', {}),
                overall_score=overall_score
            )
        except Exception as e:
            st.error(f"Error parsing response: {str(e)}")
            return self._create_empty_result()
    
    def _create_empty_result(self) -> AnalysisResult:
        return AnalysisResult(
            executive_summary="Analysis failed",
            scores=[],
            detailed_plan="",
            risk_flags=[],
            build_checklist=[],
            tech_stack={},
            pitch_deck={},
            overall_score=0.0
        )

def main():
    st.set_page_config(
        page_title="PitchSnitch",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Dark mode CSS styling
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .main .block-container {
        background-color: #0e1117;
        padding-top: 2rem;
    }
    
    .metric-container {
        background-color: #1e2329;
        border: 1px solid #3d4043;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .score-high { color: #00d4aa; }
    .score-medium { color: #ffb000; }
    .score-low { color: #ff4b4b; }
    
    .stSelectbox > div > div {
        background-color: #1e2329;
        border: 1px solid #3d4043;
    }
    
    .stTextInput > div > div > input {
        background-color: #1e2329;
        border: 1px solid #3d4043;
        color: #fafafa;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #1e2329;
        border: 1px solid #3d4043;
        color: #fafafa;
    }
    
    .stButton > button {
        background-color: #ff4b4b;
        border: none;
        color: white;
        border-radius: 0.5rem;
    }
    
    .stButton > button:hover {
        background-color: #ff6b6b;
        border: none;
    }
    
    .stExpander {
        background-color: #1e2329;
        border: 1px solid #3d4043;
        border-radius: 0.5rem;
    }
    
    .stAlert {
        background-color: #1e2329;
        border: 1px solid #3d4043;
    }
    
    .stSuccess {
        background-color: #1a2a1a;
        border: 1px solid: #00d4aa;
        color: #00d4aa;
    }
    
    .stWarning {
        background-color: #2a2a1a;
        border: 1px solid #ffb000;
        color: #ffb000;
    }
    
    .stError {
        background-color: #2a1a1a;
        border: 1px solid #ff4b4b;
        color: #ff4b4b;
    }
    
    .stInfo {
        background-color: #1a1a2a;
        border: 1px solid #4dabf7;
        color: #4dabf7;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #fafafa;
    }
    
    .stMetric > div {
        background-color: #1e2329;
        border: 1px solid #3d4043;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    .stCheckbox > label {
        color: #fafafa;
    }
    
    hr {
        border-color: #3d4043;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🎯 PitchSnitch")
    st.subheader("Transform your raw idea into a winning hackathon strategy")
    
    with st.expander("ℹ️ How it works"):
        st.write("""
        1. **Describe your idea** - Tell us about your hackathon concept
        2. **Set constraints** - Team size, time available, and goals  
        3. **Get analysis** - Claude evaluates your idea across 8 key dimensions
        4. **Review results** - See scores, risks, and a detailed implementation plan
        5. **Explore scenarios** - Test how changes might affect your approach
        """)
    
    st.divider()
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("Please set your ANTHROPIC_API_KEY environment variable")
        st.stop()
    
    coach = HackathonIdeaCoach()
    
    # Input Form
    with st.form("idea_input"):
        st.header("🎯 Tell us about your hackathon idea")
        
        idea = st.text_area(
            "Describe your hackathon idea",
            placeholder="e.g., An AI-powered tool that helps students find study groups based on their learning style and schedule",
            height=100
        )
        
        target_users = st.text_input(
            "Who are your target users?",
            placeholder="e.g., College students, working professionals, parents"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            time_constraint = st.select_slider(
                "Time available (hours)",
                options=[24, 36, 48, 60, 72],
                value=48
            )
        
        with col2:
            team_size = st.select_slider(
                "Team size",
                options=[1, 2, 3, 4, 5, 6],
                value=3
            )
        
        goals = st.text_area(
            "What are your goals for this hackathon?",
            placeholder="e.g., Build a working prototype, learn new technologies, win the competition",
            height=80
        )
        
        submitted = st.form_submit_button("🎯 Snitch My Pitch", type="primary")
    
    if submitted and idea and target_users and goals:
        idea_input = IdeaInput(idea, target_users, time_constraint, team_size, goals)
        
        with st.spinner("Analyzing your idea with Claude..."):
            result = coach.analyze_idea(idea_input)
        
        # Display Results
        if result.overall_score > 0:
            # Executive Summary
            st.header("📊 Executive Summary")
            st.success(result.executive_summary)
            
            # Overall Score
            score_color = "green" if result.overall_score >= 3.5 else "orange" if result.overall_score >= 2.5 else "red"
            st.metric("Overall Score", f"{result.overall_score:.1f}/5.0", delta=None)
            
            # Detailed Scores
            st.header("📈 Detailed Analysis")
            col1, col2 = st.columns(2)
            
            for i, score in enumerate(result.scores):
                with col1 if i % 2 == 0 else col2:
                    with st.expander(f"{score.dimension}: {score.score}/5"):
                        st.write(score.reasoning)
            
            # Detailed Plan
            st.header("🗺️ Implementation Plan")
            st.markdown(result.detailed_plan)
            
            # Risk Flags
            if result.risk_flags:
                st.header("⚠️ Risk Flags")
                for risk in result.risk_flags:
                    st.warning(risk)
            
            # Tech Stack Recommendations
            st.header("🛠️ Recommended Tech Stack")
            if result.tech_stack:
                for category, technologies in result.tech_stack.items():
                    if technologies:
                        st.subheader(f"**{category}**")
                        tech_cols = st.columns(min(len(technologies), 3))
                        for i, tech in enumerate(technologies):
                            with tech_cols[i % 3]:
                                st.markdown(f"• {tech}")
                        st.write("")
            
            # Build Checklist
            st.header("✅ 48-Hour Build Checklist")
            for i, task in enumerate(result.build_checklist, 1):
                st.checkbox(f"{i}. {task}", key=f"task_{i}")
            
            # Pitch Deck Content
            st.header("📊 5-Slide Pitch Deck")
            st.write("Comprehensive, judge-ready presentation content for your hackathon pitch:")
            
            if result.pitch_deck:
                # Slide 1: Problem
                with st.expander("🎯 Slide 1: Problem Statement", expanded=True):
                    st.markdown("### 🔍 The Problem We're Solving")
                    content = result.pitch_deck.get('slide1_problem', 'Problem statement not available')
                    # Format paragraphs for better readability
                    paragraphs = content.split('. ')
                    for i, paragraph in enumerate(paragraphs):
                        if paragraph.strip():
                            st.markdown(f"**{paragraph.strip()}.**" if i == 0 else f"{paragraph.strip()}.")
                    st.divider()
                    st.caption("💡 **Presentation Tip**: Start with a relatable scenario or shocking statistic to grab attention")
                
                # Slide 2: Solution  
                with st.expander("💡 Slide 2: Our Solution", expanded=False):
                    st.markdown("### 🚀 How We Solve It")
                    content = result.pitch_deck.get('slide2_solution', 'Solution description not available')
                    paragraphs = content.split('. ')
                    for i, paragraph in enumerate(paragraphs):
                        if paragraph.strip():
                            st.markdown(f"**{paragraph.strip()}.**" if i == 0 else f"{paragraph.strip()}.")
                    st.divider()
                    st.caption("💡 **Presentation Tip**: Demo key features live if possible, use visuals to show before/after")
                
                # Slide 3: Tech Stack
                with st.expander("🛠️ Slide 3: Technical Implementation", expanded=False):
                    st.markdown("### ⚙️ How We Built It")
                    content = result.pitch_deck.get('slide3_techstack', 'Technical details not available')
                    paragraphs = content.split('. ')
                    for i, paragraph in enumerate(paragraphs):
                        if paragraph.strip():
                            st.markdown(f"**{paragraph.strip()}.**" if i == 0 else f"{paragraph.strip()}.")
                    st.divider()
                    st.caption("💡 **Presentation Tip**: Show architecture diagrams, highlight technical challenges overcome")
                
                # Slide 4: Market
                with st.expander("📈 Slide 4: Market Opportunity", expanded=False):
                    st.markdown("### 🌍 Market & Business Impact")
                    content = result.pitch_deck.get('slide4_market', 'Market analysis not available')
                    paragraphs = content.split('. ')
                    for i, paragraph in enumerate(paragraphs):
                        if paragraph.strip():
                            st.markdown(f"**{paragraph.strip()}.**" if i == 0 else f"{paragraph.strip()}.")
                    st.divider()
                    st.caption("💡 **Presentation Tip**: Use charts for market size, mention specific customer validation")
                
                # Slide 5: Business Model
                with st.expander("💰 Slide 5: Business Strategy", expanded=False):
                    st.markdown("### 💼 How We Scale & Monetize")
                    content = result.pitch_deck.get('slide5_business_model', 'Business model not available')
                    paragraphs = content.split('. ')
                    for i, paragraph in enumerate(paragraphs):
                        if paragraph.strip():
                            st.markdown(f"**{paragraph.strip()}.**" if i == 0 else f"{paragraph.strip()}.")
                    st.divider()
                    st.caption("💡 **Presentation Tip**: Show revenue projections, explain competitive advantages clearly")
                
                st.success("🎯 **Final Pro Tips**: Keep each slide under 3 minutes, practice transitions, end with specific asks (funding, partnerships, users), and prepare for Q&A!")
            else:
                st.warning("Pitch deck content not available. Try regenerating the analysis.")
    
    # Footer
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 12px; margin-top: 1rem; padding: 10px;'>
            <p>Made with ❤️ by <strong>Geetanshi Goel</strong></p>
            <div style='margin-top: 8px;'>
                <a href="https://github.com/geetanshi0205" target="_blank" style='margin: 0 8px; text-decoration: none;'>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle;">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.30.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                </a>
                <a href="https://www.linkedin.com/in/geetanshi-goel-49ba5832b/" target="_blank" style='margin: 0 8px; text-decoration: none;'>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: middle;">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                    </svg>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()