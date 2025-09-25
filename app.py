
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Brain 2.0", layout="centered")

# --- Welcome/Personalization ---
st.title("Welcome to Brain 2.0")

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''
    st.session_state['personalisation_enabled'] = True
    st.session_state['page'] = 'personalisation'

def go_to(page):
    st.session_state['page'] = page

# --- Personalisation Page ---
if st.session_state['page'] == 'personalisation':
    with st.form("personalisation_form"):
        st.write("Personalize your experience (optional):")
        user_name = st.text_input("Enter your name (or leave blank to skip)")
        personalisation_enabled = st.checkbox("Enable personalization?", value=True)
        submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state['user_name'] = user_name
            st.session_state['personalisation_enabled'] = personalisation_enabled
            go_to('life_vibe')
            st.experimental_rerun()
    st.stop()

# --- Life-Vibe Weighting ---
if st.session_state['page'] == 'life_vibe':
    st.header("Life-Vibe Weighting")
    st.write("Rate your current focus in each area:")
    focus_areas = [
        "Monetary/Work", "Creative", "Humanitarian", "Social", "Self-care", "Learning", "Other"
    ]
    vibe_weights = {}
    with st.form("vibe_form"):
        for area in focus_areas:
            vibe_weights[area] = st.slider(f"{area} focus", 0, 5, 3)
        submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state['vibe_weights'] = vibe_weights
            go_to('reflection')
            st.experimental_rerun()
    st.stop()

# --- Reflection & Self-Assessment ---
if st.session_state['page'] == 'reflection':
    st.header("Reflection & Self-Assessment")
    st.write("How are you feeling today?")
    with st.form("reflection_form"):
        mood = st.slider("Mood", 1, 5, 3)
        energy = st.slider("Energy", 1, 5, 3)
        stress = st.slider("Stress", 1, 5, 3)
        sleep = st.slider("Sleep Quality", 1, 5, 3)
        social = st.slider("Social Connection", 1, 5, 3)
        notes = st.text_area("Any notes or reflections?")
        submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state['reflection'] = {
                'mood': mood,
                'energy': energy,
                'stress': stress,
                'sleep': sleep,
                'social': social,
                'notes': notes
            }
            go_to('goals')
            st.experimental_rerun()
    st.stop()

# --- Goal Highlighting ---
if st.session_state['page'] == 'goals':
    st.header("Goal Highlighting")
    st.write("Set and weight your goals:")
    with st.form("goals_form"):
        primary_goal = st.text_input("Primary Goal")
        primary_weight = st.slider("Primary Goal Weight", 1, 5, 3)
        secondary_goal = st.text_input("Secondary Goal")
        secondary_weight = st.slider("Secondary Goal Weight", 1, 5, 2)
        background_goal = st.text_input("Background Goal")
        background_weight = st.slider("Background Goal Weight", 1, 5, 1)
        submitted = st.form_submit_button("Continue")
        if submitted:
            st.session_state['goals'] = {
                'primary': {'goal': primary_goal, 'weight': primary_weight},
                'secondary': {'goal': secondary_goal, 'weight': secondary_weight},
                'background': {'goal': background_goal, 'weight': background_weight}
            }
            go_to('dashboard')
            st.experimental_rerun()
    st.stop()

# --- Dashboard Summary ---
if st.session_state['page'] == 'dashboard':
    st.header("Personal Dashboard Summary")
    st.write("Here’s a summary of your session:")
    st.subheader("Life-Vibe Weights")
    st.bar_chart(pd.DataFrame.from_dict(st.session_state['vibe_weights'], orient='index', columns=['Weight']))
    st.subheader("Reflection")
    st.write(st.session_state['reflection'])
    st.subheader("Goals")
    for tier, g in st.session_state['goals'].items():
        st.write(f"{tier.capitalize()}: {g['goal']} (Weight: {g['weight']}/5)")
    if st.button("Finish & See Big Pitch"):
        go_to('big_pitch')
        st.experimental_rerun()
    st.stop()

# --- Big Pitch Recap ---
if st.session_state['page'] == 'big_pitch':
    st.header("The Big Pitch: Why This Matters")
    st.markdown("""
    Imagine waking up and actually feeling in sync with your own life—not just chasing tasks, but seeing real progress, catching burnout before it starts, and having a system that adapts to you, not the other way around.

    This isn’t just another productivity tool. This is about building a real, living feedback loop for your mind, your energy, your goals, and your wellbeing.

    **How does it all tie together?**
    - Every check-in, reflection, and goal you set feeds into your dashboard, giving you a living map of your progress and patterns.
    - The habit tracker, focus sprints, and creativity check-ins aren’t just isolated features—they’re all connected, so you can see how your energy, mood, and habits influence each other.
    - Nudges and micro-tutorials are personalized, triggered by your real data, so you get the right support at the right time.
    - The recap and expanded info help you zoom out, spot trends, and make smarter decisions for the week ahead.
    - As the community grows, anonymized insights will help everyone see what’s working for people like them—turning individual progress into collective wisdom.
    - The more you use it, the more powerful it gets: your data, your patterns, your feedback all feed into a smarter, more supportive system for everyone.

    **The Data & Insights Arm: Why It’s a Game-Changer**
    - With user consent, anonymized data can power research into what really helps people avoid burnout, build habits, and stay on track.
    - We can surface trends: What habits help most with energy? What reflection prompts lead to the biggest breakthroughs?
    - Imagine a dashboard for the whole community: ‘This week, people who did X habit saw a 20% boost in mood.’
    - This data can be used to create new features, smarter nudges, and even open up partnerships with researchers, wellness orgs, and companies who want to support their people better.
    - There’s huge value in being able to say: ‘Here’s what actually works, for real people, in the real world.’
    - Long-term, the data arm could become a revenue stream itself—offering anonymized, ethical insights to organizations, or powering new AI-driven tools for users.
    - The data also helps us build a feedback loop: the more we learn, the better we can help you (and everyone else) grow.

    **What are the real benefits?**
    - Spot burnout before it hits: Get early warnings when your energy, mood, or habits start to slip.
    - See your progress, not just your to-dos: Visual dashboards and recaps show you how far you’ve come, not just what’s left to do.
    - Adapt to real life: The system learns your rhythms—if you’re having a rough week, it helps you adjust, not guilt-trip you.
    - Build habits that stick: Track, tweak, and celebrate small wins so you actually build momentum.
    - Get nudges that matter: Contextual tips and encouragements based on your real data, not generic advice.
    - Feel less alone: Community features (coming soon) let you share, learn, and get support from people on the same journey.
    - Make better decisions: See patterns in your mood, energy, and focus so you can plan smarter, not harder.
    - Save time and mental energy: Automated recaps, reminders, and insights mean less mental clutter and more clarity.
    - Use your data for good: Opt in to help power research, new features, and collective breakthroughs.

    **The User Journey: From Day One to Year One**
    - Day 1: You start with a simple check-in. Maybe you’re feeling a bit off, or maybe you’re just curious.
    - Week 1: You notice patterns—your energy dips on Wednesdays, your mood lifts after creative sprints.
    - Month 1: You’ve built a couple of habits, dodged a burnout spiral, and started using the dashboard to plan your week.
    - Month 3: You’re part of a challenge group, sharing tips and wins, and you’ve got a streak going.
    - Month 6: You’ve got a year’s worth of insights, and you’re helping shape new features with your feedback.
    - Year 1: You look back and see real, measurable growth—not just in your goals, but in your resilience, your self-awareness, and your ability to adapt.

    **The Business & Impact Vision**
    1. Quick Revenue Streams:
        - Early supporter memberships: For a few pounds a month, get access to new features, community, and direct input into the roadmap.
        - Pay-what-you-want upgrades: Unlock custom dashboards, extra analytics, or AI-powered nudges for whatever you think it’s worth.
        - Microtransactions: Buy a one-off deep-dive report, a printable journal, or a custom theme.
        - Donation/support buttons: If you love it, you can just chip in.
        - Live workshops and group challenges: Pay to join a focused sprint, a habit bootcamp, or a live Q&A with experts.
    2. Long-Term, Scalable Revenue:
        - Premium analytics: Monthly or annual subscriptions for advanced tracking, trend analysis, and AI-driven insights.
        - Corporate wellness: Sell team dashboards and group analytics to companies who want to support their staff.
        - Licensing: Let coaches, therapists, and organizations use the platform with their own clients.
        - Affiliate partnerships: Earn commission by recommending books, courses, or wellness products that actually help.
        - Content revenue: Monetize YouTube videos, podcasts, and written guides that teach people how to get the most out of the system.
        - Merch and printables: Sell branded journals, habit trackers, or even fun swag for the community.
        - API access: Let other apps and platforms plug into the system for a fee.
        - Data insights: (With consent) offer anonymized, ethical trend reports to organizations or researchers.
    **Example scenarios:**
    - A user pays £5 for a custom monthly recap PDF they can share with their therapist or coach.
    - A company pays £99/month for a team dashboard that helps their staff avoid burnout and stay engaged.
    - A coach licenses the platform for their 1:1 clients, adding value to their own business.
    - A group of users join a paid 30-day challenge to build a new habit together, with live check-ins and rewards.
    - Someone buys a physical journal or printable to use offline, supporting the project and spreading the word.
    - A university or wellness org pays for anonymized trend data to improve their own programs.
    3. Why It’s Built to Succeed:
        - No big team, no burn rate: My own skills and passion are always free to the project. I’ll handle the tech, content, and groundwork myself for the first few months—so there’s no pressure to chase funding or rack up costs.
        - Fast iteration: We can experiment, launch, and adapt quickly, based on real user feedback—not just guesses.
        - Community-first: Every feature is designed to help people help each other, not just themselves.
        - Real impact: The more people use it, the more valuable the insights and support become—for everyone.
        - Data-driven: The more we learn, the more we can help—every user, every organization, every new feature.

    **The Future We Can Build**
    Picture this: A year from now, thousands of people are using this system to stay on track, avoid burnout, and actually enjoy the process of growth. They’re sharing what works, supporting each other, and building a movement around self-awareness and sustainable progress.

    The project is self-sustaining, with a steady stream of revenue from people who genuinely value what it offers. There’s no pressure to sell out, no need to chase investors or ads. Just a growing, thriving community—and the freedom to keep making it better, together.

    If you’re reading this, you’re not just a user—you’re a co-creator. Your feedback, your ideas, and your energy are what will make this work.

    Let’s build something that actually makes a difference. Let’s make self-reflection, progress tracking, and real support the new normal.
    """)
