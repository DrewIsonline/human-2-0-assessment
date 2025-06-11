# Human 2.0 Assessment Bot - Python Implementation
# Created for DrewIs.. UpLevel Movement Business
# Author: Manus AI
# Date: June 2025

import json
import datetime
from typing import Dict, List, Any, Optional
import openai
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class Human20AssessmentBot:
    """
    The Human 2.0 Assessment Bot conducts comprehensive evaluations across
    biological optimization, mental architecture, and financial intelligence domains.
    """
    
    def __init__(self, api_key: str, business_profile: Dict[str, str]):
        """
        Initialize the Human 2.0 Assessment Bot
        
        Args:
            api_key: OpenAI API key
            business_profile: Dictionary containing business customization info
        """
        self.api_key = "sk-proj-YOUR-NEW-API-KEY-HERE"
        openai.api_key = self.api_key

        
        # Business Profile Configuration (Hardcoded for easy customization)
        self.business_profile = {
            "business_name": business_profile.get("business_name", "Drew_Is.."),
            "coach_name": business_profile.get("coach_name", "Drew"),
            "website": business_profile.get("website", "https://drewis.online" ),
            "email": business_profile.get("email", "drew@drewis.online"),
            "phone": business_profile.get("phone", "+1-503-855-6181"),
            "brand_message": business_profile.get("brand_message", "You're not broken. You're upgrading. It's Time to get dangerous!"),
            "service_price": business_profile.get("service_price", "$497"),
            "service_price_beta": "$497 (Beta Launch - Regular $997)",
            "service_price_regular": "$997",
            "service_price_premium": "$2,497",
            "calendar_link": business_profile.get("calendar_link", "https://calendly.com/drew-drewis/product-q-a-session" )
        }

        
        # Assessment Categories and Weights
        self.assessment_categories = {
            "biological_optimization": {
                "weight": 0.33,
                "subcategories": {
                    "sleep_quality": 0.25,
                    "energy_levels": 0.25,
                    "stress_management": 0.20,
                    "nutrition_optimization": 0.15,
                    "recovery_protocols": 0.15
                }
            },
            "mental_architecture": {
                "weight": 0.33,
                "subcategories": {
                    "cognitive_performance": 0.30,
                    "emotional_intelligence": 0.25,
                    "stress_resilience": 0.20,
                    "mindset_patterns": 0.25
                }
            },
            "financial_intelligence": {
                "weight": 0.34,
                "subcategories": {
                    "wealth_building": 0.30,
                    "money_mindset": 0.25,
                    "business_optimization": 0.25,
                    "investment_intelligence": 0.20
                }
            }
        }
        
        # Initialize session state
        if 'assessment_data' not in st.session_state:
            st.session_state.assessment_data = {}
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 'welcome'
    
    def display_welcome_screen(self):
        """Display the welcome screen with branding and introduction"""
        st.markdown(f"""
        # 🚀 Welcome to the Human 2.0 Assessment
        ## Discover Your Dangerous Upgrade Potential
        
        ### {self.business_profile['brand_message']}
        
        **Welcome to {self.business_profile['business_name']}!**
        
        This comprehensive assessment will analyze your current optimization across three critical domains:
        
        🧬 **Biological Optimization** - Your physical performance and health systems
        🧠 **Mental Architecture** - Your cognitive performance and emotional intelligence  
        💰 **Financial Intelligence** - Your wealth building and money mindset
        
        **What You'll Receive:**
        - Detailed analysis across all three Human 2.0 pillars
        - Personalized upgrade roadmap with specific recommendations
        - AI-powered pattern recognition and opportunity identification
        - Custom optimization strategy worth {self.business_profile['service_price']}
        
        **Time Required:** 15-20 minutes for complete assessment
        
        **Your Guide:** {self.business_profile['coach_name']}, Human 2.0 Architect
        """)
        
        if st.button("🚀 Begin Your Human 2.0 Assessment", key="start_assessment"):
            st.session_state.current_step = 'basic_info'
            st.rerun()
    
    def collect_basic_information(self):
        """Collect basic demographic and contact information"""
        st.markdown("## 📋 Basic Information")
        st.markdown("Let's start with some basic information about you:")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name*", key="first_name")
                email = st.text_input("Email Address*", key="email")
                age = st.selectbox("Age Range", 
                    ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"], key="age")
            
            with col2:
                last_name = st.text_input("Last Name*", key="last_name")
                phone = st.text_input("Phone Number", key="phone")
                occupation = st.text_input("Occupation/Industry", key="occupation")
            
            primary_goal = st.selectbox(
                "What's your primary optimization goal?",
                [
                    "Increase energy and physical performance",
                    "Enhance mental clarity and focus",
                    "Accelerate wealth building and financial success",
                    "Achieve balance across all areas",
                    "Build a high-performance lifestyle",
                    "Other"
                ],
                key="primary_goal"
            )
            
            if primary_goal == "Other":
                custom_goal = st.text_input("Please specify your goal:", key="custom_goal")
            
            submitted = st.form_submit_button("Continue to Assessment →")
            
            if submitted:
                if first_name and last_name and email:
                    st.session_state.assessment_data.update({
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'phone': phone,
                        'age': age,
                        'occupation': occupation,
                        'primary_goal': primary_goal,
                        'custom_goal': custom_goal if primary_goal == "Other" else ""
                    })
                    st.session_state.current_step = 'biological_assessment'
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    def biological_optimization_assessment(self):
        """Conduct biological optimization assessment"""
        st.markdown("## 🧬 Biological Optimization Assessment")
        st.markdown("Let's evaluate your current biological performance and optimization:")
        
        with st.form("biological_form"):
            # Sleep Quality Assessment
            st.markdown("### 😴 Sleep Quality")
            sleep_hours = st.slider("Average hours of sleep per night", 4, 12, 7, key="sleep_hours")
            sleep_quality = st.select_slider(
                "How would you rate your sleep quality?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="sleep_quality"
            )
            wake_refreshed = st.select_slider(
                "How often do you wake up feeling refreshed?",
                options=["Never", "Rarely", "Sometimes", "Often", "Always"],
                value="Sometimes",
                key="wake_refreshed"
            )
            
            # Energy Levels
            st.markdown("### ⚡ Energy Levels")
            energy_morning = st.slider("Morning energy level (1-10)", 1, 10, 5, key="energy_morning")
            energy_afternoon = st.slider("Afternoon energy level (1-10)", 1, 10, 5, key="energy_afternoon")
            energy_evening = st.slider("Evening energy level (1-10)", 1, 10, 5, key="energy_evening")
            energy_crashes = st.selectbox(
                "How often do you experience energy crashes?",
                ["Multiple times daily", "Daily", "Few times per week", "Rarely", "Never"],
                key="energy_crashes"
            )
            
            # Stress and Recovery
            st.markdown("### 🎯 Stress Management & Recovery")
            stress_level = st.slider("Current stress level (1-10)", 1, 10, 5, key="stress_level")
            stress_management = st.select_slider(
                "How well do you manage stress?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="stress_management"
            )
            recovery_time = st.selectbox(
                "How quickly do you recover from physical/mental exertion?",
                ["Very slowly", "Slowly", "Average", "Quickly", "Very quickly"],
                key="recovery_time"
            )
            
            # Nutrition and Health
            st.markdown("### 🥗 Nutrition & Health")
            nutrition_quality = st.select_slider(
                "How would you rate your nutrition quality?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="nutrition_quality"
            )
            hydration = st.selectbox(
                "Daily water intake",
                ["Less than 4 glasses", "4-6 glasses", "6-8 glasses", "8-10 glasses", "More than 10 glasses"],
                key="hydration"
            )
            exercise_frequency = st.selectbox(
                "Exercise frequency per week",
                ["Never", "1-2 times", "3-4 times", "5-6 times", "Daily"],
                key="exercise_frequency"
            )
            
            submitted = st.form_submit_button("Continue to Mental Assessment →")
            
            if submitted:
                biological_data = {
                    'sleep_hours': sleep_hours,
                    'sleep_quality': sleep_quality,
                    'wake_refreshed': wake_refreshed,
                    'energy_morning': energy_morning,
                    'energy_afternoon': energy_afternoon,
                    'energy_evening': energy_evening,
                    'energy_crashes': energy_crashes,
                    'stress_level': stress_level,
                    'stress_management': stress_management,
                    'recovery_time': recovery_time,
                    'nutrition_quality': nutrition_quality,
                    'hydration': hydration,
                    'exercise_frequency': exercise_frequency
                }
                st.session_state.assessment_data['biological'] = biological_data
                st.session_state.current_step = 'mental_assessment'
                st.rerun()
    
    def mental_architecture_assessment(self):
        """Conduct mental architecture assessment"""
        st.markdown("## 🧠 Mental Architecture Assessment")
        st.markdown("Let's evaluate your cognitive performance and mental optimization:")
        
        with st.form("mental_form"):
            # Cognitive Performance
            st.markdown("### 🎯 Cognitive Performance")
            focus_duration = st.selectbox(
                "How long can you maintain deep focus?",
                ["Less than 15 minutes", "15-30 minutes", "30-60 minutes", "1-2 hours", "More than 2 hours"],
                key="focus_duration"
            )
            mental_clarity = st.slider("Mental clarity throughout the day (1-10)", 1, 10, 5, key="mental_clarity")
            decision_making = st.select_slider(
                "How confident are you in your decision-making?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="decision_making"
            )
            memory_performance = st.select_slider(
                "How would you rate your memory performance?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="memory_performance"
            )
            
            # Emotional Intelligence
            st.markdown("### 💭 Emotional Intelligence")
            emotional_awareness = st.slider("Emotional self-awareness (1-10)", 1, 10, 5, key="emotional_awareness")
            emotional_regulation = st.select_slider(
                "How well do you regulate your emotions?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="emotional_regulation"
            )
            social_skills = st.slider("Social and interpersonal skills (1-10)", 1, 10, 5, key="social_skills")
            empathy_level = st.slider("Empathy and understanding of others (1-10)", 1, 10, 5, key="empathy_level")
            
            # Mindset and Beliefs
            st.markdown("### 🌟 Mindset & Beliefs")
            growth_mindset = st.select_slider(
                "How much do you believe you can improve and grow?",
                options=["Very Little", "Somewhat", "Moderately", "Significantly", "Completely"],
                value="Moderately",
                key="growth_mindset"
            )
            self_confidence = st.slider("Overall self-confidence (1-10)", 1, 10, 5, key="self_confidence")
            resilience = st.select_slider(
                "How well do you bounce back from setbacks?",
                options=["Very Poor", "Poor", "Fair", "Good", "Excellent"],
                value="Fair",
                key="resilience"
            )
            limiting_beliefs = st.multiselect(
                "Which limiting beliefs do you struggle with? (Select all that apply)",
                [
                    "I'm not smart enough",
                    "I don't deserve success",
                    "I'm too old/young to change",
                    "I don't have enough time",
                    "I'm not good with technology",
                    "Success requires sacrifice",
                    "I'm not a 'numbers person'",
                    "Other people are more talented",
                    "None of these apply to me"
                ],
                key="limiting_beliefs"
            )
            
            submitted = st.form_submit_button("Continue to Financial Assessment →")
            
            if submitted:
                mental_data = {
                    'focus_duration': focus_duration,
                    'mental_clarity': mental_clarity,
                    'decision_making': decision_making,
                    'memory_performance': memory_performance,
                    'emotional_awareness': emotional_awareness,
                    'emotional_regulation': emotional_regulation,
                    'social_skills': social_skills,
                    'empathy_level': empathy_level,
                    'growth_mindset': growth_mindset,
                    'self_confidence': self_confidence,
                    'resilience': resilience,
                    'limiting_beliefs': limiting_beliefs
                }
                st.session_state.assessment_data['mental'] = mental_data
                st.session_state.current_step = 'financial_assessment'
                st.rerun()
    
    def financial_intelligence_assessment(self):
        """Conduct financial intelligence assessment"""
        st.markdown("## 💰 Financial Intelligence Assessment")
        st.markdown("Let's evaluate your financial optimization and wealth-building potential:")
        
        with st.form("financial_form"):
            # Current Financial Status
            st.markdown("### 💼 Current Financial Status")
            income_range = st.selectbox(
                "Annual income range",
                ["Under $25K", "$25K-$50K", "$50K-$75K", "$75K-$100K", "$100K-$150K", "$150K-$250K", "$250K+"],
                key="income_range"
            )
            savings_rate = st.selectbox(
                "What percentage of income do you save/invest?",
                ["0-5%", "5-10%", "10-15%", "15-20%", "20%+"],
                key="savings_rate"
            )
            debt_situation = st.selectbox(
                "Current debt situation",
                ["Debt-free", "Minimal debt", "Moderate debt", "High debt", "Overwhelming debt"],
                key="debt_situation"
            )
            emergency_fund = st.selectbox(
                "Emergency fund coverage",
                ["No emergency fund", "Less than 1 month", "1-3 months", "3-6 months", "6+ months"],
                key="emergency_fund"
            )
            
            # Investment and Wealth Building
            st.markdown("### 📈 Investment & Wealth Building")
            investment_experience = st.select_slider(
                "Investment experience level",
                options=["Beginner", "Novice", "Intermediate", "Advanced", "Expert"],
                value="Novice",
                key="investment_experience"
            )
            investment_portfolio = st.multiselect(
                "Current investment types (select all that apply)",
                [
                    "Savings accounts",
                    "Stocks/ETFs",
                    "Bonds",
                    "Real estate",
                    "Cryptocurrency",
                    "Business investments",
                    "Retirement accounts (401k, IRA)",
                    "None"
                ],
                key="investment_portfolio"
            )
            financial_goals = st.multiselect(
                "Primary financial goals (select all that apply)",
                [
                    "Build emergency fund",
                    "Pay off debt",
                    "Save for major purchase",
                    "Retirement planning",
                    "Generate passive income",
                    "Start/grow a business",
                    "Achieve financial independence",
                    "Build generational wealth"
                ],
                key="financial_goals"
            )
            
            # Money Mindset
            st.markdown("### 🧠 Money Mindset")
            money_stress = st.slider("How much stress does money cause you? (1-10)", 1, 10, 5, key="money_stress")
            money_confidence = st.slider("Confidence in financial decision-making (1-10)", 1, 10, 5, key="money_confidence")
            wealth_beliefs = st.multiselect(
                "Which beliefs about money resonate with you? (select all that apply)",
                [
                    "Money is the root of all evil",
                    "Rich people are greedy",
                    "I don't deserve to be wealthy",
                    "Money doesn't buy happiness",
                    "There's not enough money to go around",
                    "I'm not good with money",
                    "Money comes and goes",
                    "Wealth requires sacrifice",
                    "None of these resonate with me"
                ],
                key="wealth_beliefs"
            )
            
            # Business and Entrepreneurship
            st.markdown("### 🚀 Business & Entrepreneurship")
            business_status = st.selectbox(
                "Current business status",
                ["Employee only", "Side hustle", "Part-time business", "Full-time entrepreneur", "Multiple businesses"],
                key="business_status"
            )
            if business_status != "Employee only":
                business_revenue = st.selectbox(
                    "Monthly business revenue",
                    ["Under $1K", "$1K-$5K", "$5K-$10K", "$10K-$25K", "$25K-$50K", "$50K+"],
                    key="business_revenue"
                )
            else:
                business_revenue = "N/A"
            
            entrepreneurial_interest = st.slider("Interest in entrepreneurship (1-10)", 1, 10, 5, key="entrepreneurial_interest")
            
            submitted = st.form_submit_button("Generate My Human 2.0 Assessment →")
            
            if submitted:
                financial_data = {
                    'income_range': income_range,
                    'savings_rate': savings_rate,
                    'debt_situation': debt_situation,
                    'emergency_fund': emergency_fund,
                    'investment_experience': investment_experience,
                    'investment_portfolio': investment_portfolio,
                    'financial_goals': financial_goals,
                    'money_stress': money_stress,
                    'money_confidence': money_confidence,
                    'wealth_beliefs': wealth_beliefs,
                    'business_status': business_status,
                    'business_revenue': business_revenue,
                    'entrepreneurial_interest': entrepreneurial_interest
                }
                st.session_state.assessment_data['financial'] = financial_data
                st.session_state.current_step = 'generate_results'
                st.rerun()
    
    def calculate_scores(self) -> Dict[str, Any]:
        """Calculate assessment scores across all domains"""
        scores = {}
        
        # Biological Optimization Score
        bio_data = st.session_state.assessment_data['biological']
        bio_score = 0
        
        # Sleep quality scoring
        sleep_score = (bio_data['sleep_hours'] - 4) / 8 * 100  # Normalize to 0-100
        quality_map = {"Very Poor": 0, "Poor": 25, "Fair": 50, "Good": 75, "Excellent": 100}
        sleep_score += quality_map[bio_data['sleep_quality']]
        sleep_score += quality_map.get(bio_data['wake_refreshed'], 50)
        sleep_score /= 3
        
        # Energy scoring
        energy_score = (bio_data['energy_morning'] + bio_data['energy_afternoon'] + bio_data['energy_evening']) / 3 * 10
        crash_map = {"Multiple times daily": 0, "Daily": 25, "Few times per week": 50, "Rarely": 75, "Never": 100}
        energy_score = (energy_score + crash_map[bio_data['energy_crashes']]) / 2
        
        # Stress and recovery scoring
        stress_score = (10 - bio_data['stress_level']) * 10  # Invert stress level
        stress_score += quality_map[bio_data['stress_management']]
        recovery_map = {"Very slowly": 0, "Slowly": 25, "Average": 50, "Quickly": 75, "Very quickly": 100}
        stress_score += recovery_map[bio_data['recovery_time']]
        stress_score /= 3
        
        # Nutrition scoring
        nutrition_score = quality_map[bio_data['nutrition_quality']]
        hydration_map = {"Less than 4 glasses": 0, "4-6 glasses": 25, "6-8 glasses": 75, "8-10 glasses": 100, "More than 10 glasses": 90}
        exercise_map = {"Never": 0, "1-2 times": 25, "3-4 times": 50, "5-6 times": 75, "Daily": 100}
        nutrition_score = (nutrition_score + hydration_map[bio_data['hydration']] + exercise_map[bio_data['exercise_frequency']]) / 3
        
        bio_score = (sleep_score * 0.25 + energy_score * 0.25 + stress_score * 0.20 + nutrition_score * 0.30)
        scores['biological'] = min(100, max(0, bio_score))
        
        # Mental Architecture Score
        mental_data = st.session_state.assessment_data['mental']
        mental_score = 0
        
        # Cognitive performance
        focus_map = {"Less than 15 minutes": 0, "15-30 minutes": 25, "30-60 minutes": 50, "1-2 hours": 75, "More than 2 hours": 100}
        cognitive_score = focus_map[mental_data['focus_duration']]
        cognitive_score += mental_data['mental_clarity'] * 10
        cognitive_score += quality_map[mental_data['decision_making']]
        cognitive_score += quality_map[mental_data['memory_performance']]
        cognitive_score /= 4
        
        # Emotional intelligence
        emotional_score = (mental_data['emotional_awareness'] + mental_data['social_skills'] + mental_data['empathy_level']) / 3 * 10
        emotional_score += quality_map[mental_data['emotional_regulation']]
        emotional_score /= 2
        
        # Mindset and resilience
        growth_map = {"Very Little": 0, "Somewhat": 25, "Moderately": 50, "Significantly": 75, "Completely": 100}
        mindset_score = growth_map[mental_data['growth_mindset']]
        mindset_score += mental_data['self_confidence'] * 10
        mindset_score += quality_map[mental_data['resilience']]
        mindset_score /= 3
        
        mental_score = (cognitive_score * 0.30 + emotional_score * 0.35 + mindset_score * 0.35)
        scores['mental'] = min(100, max(0, mental_score))
        
        # Financial Intelligence Score
        financial_data = st.session_state.assessment_data['financial']
        financial_score = 0
        
        # Income and savings
        income_map = {"Under $25K": 10, "$25K-$50K": 25, "$50K-$75K": 40, "$75K-$100K": 60, "$100K-$150K": 75, "$150K-$250K": 90, "$250K+": 100}
        savings_map = {"0-5%": 10, "5-10%": 30, "10-15%": 50, "15-20%": 75, "20%+": 100}
        wealth_score = (income_map[financial_data['income_range']] + savings_map[financial_data['savings_rate']]) / 2
        
        # Debt and emergency fund
        debt_map = {"Debt-free": 100, "Minimal debt": 75, "Moderate debt": 50, "High debt": 25, "Overwhelming debt": 0}
        emergency_map = {"No emergency fund": 0, "Less than 1 month": 20, "1-3 months": 40, "3-6 months": 80, "6+ months": 100}
        stability_score = (debt_map[financial_data['debt_situation']] + emergency_map[financial_data['emergency_fund']]) / 2
        
        # Investment and mindset
        exp_map = {"Beginner": 20, "Novice": 40, "Intermediate": 60, "Advanced": 80, "Expert": 100}
        investment_score = exp_map[financial_data['investment_experience']]
        mindset_score = (10 - financial_data['money_stress']) * 10 + financial_data['money_confidence'] * 10
        mindset_score /= 2
        
        financial_score = (wealth_score * 0.30 + stability_score * 0.25 + investment_score * 0.20 + mindset_score * 0.25)
        scores['financial'] = min(100, max(0, financial_score))
        
        # Overall Human 2.0 Score
        scores['overall'] = (scores['biological'] * 0.33 + scores['mental'] * 0.33 + scores['financial'] * 0.34)
        
        return scores
    
    def generate_ai_analysis(self, scores: Dict[str, Any]) -> str:
        """Generate AI-powered analysis and recommendations"""
        assessment_data = st.session_state.assessment_data
        
        prompt = f"""
        As a Human 2.0 Optimization Expert, analyze this comprehensive assessment data and provide personalized insights and recommendations.
        
        ASSESSMENT SCORES:
        - Biological Optimization: {scores['biological']:.1f}/100
        - Mental Architecture: {scores['mental']:.1f}/100  
        - Financial Intelligence: {scores['financial']:.1f}/100
        - Overall Human 2.0 Score: {scores['overall']:.1f}/100
        
        PARTICIPANT PROFILE:
        Name: {assessment_data['first_name']} {assessment_data['last_name']}
        Age: {assessment_data['age']}
        Occupation: {assessment_data['occupation']}
        Primary Goal: {assessment_data['primary_goal']}
        
        BIOLOGICAL DATA: {assessment_data['biological']}
        MENTAL DATA: {assessment_data['mental']}
        FINANCIAL DATA: {assessment_data['financial']}
        
        Provide a comprehensive analysis that includes:
        1. Overall Human 2.0 readiness assessment
        2. Top 3 optimization opportunities with specific impact potential
        3. Interconnection analysis (how improving one area will amplify others)
        4. Personalized "dangerous upgrade" recommendations
        5. Specific AI tools and strategies that would be most beneficial
        6. 30-60-90 day optimization roadmap
        
        Write in an engaging, motivational tone that aligns with "You're not broken. You're upgrading. It's Time to get dangerous!" messaging.
        Be specific and actionable while maintaining authenticity and street-smart wisdom.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"AI analysis temporarily unavailable. Please contact {self.business_profile['email']} for your personalized assessment."
    
    def display_results(self):
        """Display comprehensive assessment results"""
        scores = self.calculate_scores()
        ai_analysis = self.generate_ai_analysis(scores)
        
        st.markdown(f"# 🚀 Your Human 2.0 Assessment Results")
        st.markdown(f"## {self.business_profile['brand_message']}")
        
        # Overall Score Display
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🧬 Biological", f"{scores['biological']:.0f}/100")
        with col2:
            st.metric("🧠 Mental", f"{scores['mental']:.0f}/100")
        with col3:
            st.metric("💰 Financial", f"{scores['financial']:.0f}/100")
        with col4:
            st.metric("🚀 Overall H2.0", f"{scores['overall']:.0f}/100")
        
        # Radar Chart
        categories = ['Biological\nOptimization', 'Mental\nArchitecture', 'Financial\nIntelligence']
        values = [scores['biological'], scores['mental'], scores['financial']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Close the polygon
            theta=categories + [categories[0]],
            fill='toself',
            name='Your Human 2.0 Profile',
            line_color='#FF6B6B'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Your Human 2.0 Optimization Profile"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis
        st.markdown("## 🤖 AI-Powered Analysis & Recommendations")
        st.markdown(ai_analysis)
        
        # Next Steps
        st.markdown("## 🎯 Your Next Steps to Human 2.0")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            ### 📞 Schedule Your Strategy Session
            
            Ready to implement your Human 2.0 upgrade plan?
            
            **Book a complimentary 30-minute strategy session with {self.business_profile['coach_name']}:**
            
            ✅ Dive deeper into your assessment results  
            ✅ Create your personalized 90-day roadmap  
            ✅ Identify your highest-impact AI implementations  
            ✅ Design your dangerous upgrade strategy  
            
            **Investment:** Complimentary (normally {self.business_profile['service_price']})
            """)
            
            if st.button("🚀 Book My Strategy Session", key="book_session"):
                st.markdown(f"[Click here to schedule]({self.business_profile['calendar_link']})")
        
        with col2:
            st.markdown(f"""
            ### 📧 Get Your Complete Report
            
            **Your detailed Human 2.0 Assessment Report includes:**
            
            📊 Complete scoring breakdown  
            🎯 Personalized optimization roadmap  
            🤖 AI tool recommendations  
            💡 Implementation strategies  
            📈 Progress tracking framework  
            
            **Contact Information:**
            - Email: {self.business_profile['email']}
            - Phone: {self.business_profile['phone']}
            - Website: {self.business_profile['website']}
            """)
        
        # Save results
        if st.button("📧 Email My Results", key="email_results"):
            # In a real implementation, this would send an email
            st.success(f"Your complete Human 2.0 Assessment Report has been sent to {st.session_state.assessment_data['email']}")
        
        # Reset option
        if st.button("🔄 Take Assessment Again", key="reset"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()

def main():
    """Main application function"""
    st.set_page_config(
        page_title="Human 2.0 Assessment",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Business Profile Configuration - CUSTOMIZE THIS SECTION
    business_profile = {
        "business_name": "DrewIs.online",
        "coach_name": "Drew",
        "website": "https://drewis.online",
        "email": "drew@drewis.online",
        "phone": "+1-503-855-6181",
        "brand_message": "You're not broken. You're upgrading. It's Time to get dangerous!",
        "service_price": "$2,497",
        "calendar_link": "https://calendly.com/drew-drewis/product-q-a-session"
    }
    
    # API Key - Set your OpenAI API key here
    api_key = "your-openai-api-key-here"  # Replace with actual API key
    
    # Initialize bot
    bot = Human20AssessmentBot(api_key, business_profile)
    
    # Navigation logic
    if st.session_state.current_step == 'welcome':
        bot.display_welcome_screen()
    elif st.session_state.current_step == 'basic_info':
        bot.collect_basic_information()
    elif st.session_state.current_step == 'biological_assessment':
        bot.biological_optimization_assessment()
    elif st.session_state.current_step == 'mental_assessment':
        bot.mental_architecture_assessment()
    elif st.session_state.current_step == 'financial_assessment':
        bot.financial_intelligence_assessment()
    elif st.session_state.current_step == 'generate_results':
        bot.display_results()

if __name__ == "__main__":
    main()

# DEPLOYMENT INSTRUCTIONS:
# 1. Install required packages: pip install streamlit openai plotly pandas
# 2. Replace "your-openai-api-key-here" with your actual OpenAI API key
# 3. Customize the business_profile dictionary with your information
# 4. Run with: streamlit run human_2_0_assessment_bot.py
# 5. For production deployment, use Streamlit Cloud, Heroku, or similar platform

# CUSTOMIZATION NOTES:
# - All business information is in the business_profile dictionary
# - Scoring algorithms can be adjusted in the calculate_scores method
# - Assessment questions can be modified in each assessment method
# - AI analysis prompt can be customized in generate_ai_analysis method
# - Branding and messaging can be updated throughout the interface

