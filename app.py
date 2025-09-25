import time

def typewriter(text, delay=0.03, markdown=True):
    """Display text with a typewriter effect in Streamlit, in correct order with other content."""
    with st.container():
        slot = st.empty()
        out = ""
        for char in text:
            out += char
            if markdown:
                slot.markdown(out)
            else:
                slot.write(out)
            time.sleep(delay)
        if markdown:
            slot.markdown(out)
        else:
            slot.write(out)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Brain 2.0", layout="centered")

# --- Welcome/Personalization ---
st.title("Welcome to Brain 2.0")

if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ''
    st.session_state['personalisation_enabled'] = True
    st.session_state['page'] = 'personalisation'

def get_greeting():
    if st.session_state.get('personalisation_enabled', False) and st.session_state.get('user_name', '').strip():
        return f"Hi {st.session_state['user_name']}!"
    else:
        return "Hi there!"

def go_to(page):
    st.session_state['page'] = page


def page_personalisation():
    st.markdown("# Personalisation")
    st.markdown("_Why? Personalisation helps tailor your experience and makes your dashboard and feedback more relevant. You can skip this if you prefer to stay anonymous._")
    st.markdown("Personalize your experience (optional):")
    user_name = st.text_input("Enter your name (or leave blank to skip)", key="personalisation_name")
    personalisation_enabled = st.checkbox("Enable personalization?", key="personalisation_enabled")
    if st.button("Continue", key="personalisation_continue"):
        st.session_state['user_name'] = user_name
        go_to('life_vibe')
        st.rerun()
        return
    st.stop()


def page_life_vibe():
    st.markdown("# Life-Vibe Weighting")
    st.markdown(get_greeting())
    st.markdown("_Why? This section helps you reflect on which areas of your life are most important to you right now. Your choices shape your dashboard and help you track balance over time._")
    st.markdown("Rate your current focus in each area:")
    focus_areas = [
        "Monetary/Work", "Creative", "Humanitarian", "Social", "Self-care", "Learning", "Other"
    ]
    vibe_weights = {}
    for area in focus_areas:
        vibe_weights[area] = st.slider(f"{area} focus", 0, 5, 3, key=f"vibe_{area}")
    if st.button("Continue", key="vibe_continue"):
        st.session_state['vibe_weights'] = vibe_weights
        go_to('reflection')
        st.rerun()
        return


def page_reflection():
    st.markdown("# Reflection & Self-Assessment")
    st.markdown(get_greeting())
    st.markdown("_Why? Regular reflection helps you spot patterns in mood, energy, and stress. This data powers your dashboard and helps you catch burnout or celebrate progress._")
    st.markdown("How are you feeling today?")
    mood = st.slider("Mood", 1, 5, 3, key="reflection_mood")
    energy = st.slider("Energy", 1, 5, 3, key="reflection_energy")
    stress = st.slider("Stress", 1, 5, 3, key="reflection_stress")
    sleep = st.slider("Sleep Quality", 1, 5, 3, key="reflection_sleep")
    social = st.slider("Social Connection", 1, 5, 3, key="reflection_social")
    notes = st.text_area("Any notes or reflections?", key="reflection_notes")
    if st.button("Continue", key="reflection_continue"):
        st.session_state['reflection'] = {
            'mood': mood,
            'energy': energy,
            'stress': stress,
            'sleep': sleep,
            'social': social,
            'notes': notes
        }
        go_to('goals')
        st.rerun()
        return


def page_goals():
    st.markdown("# Goal Highlighting")
    st.markdown(get_greeting())
    st.markdown("_Why? Setting and weighting goals helps you focus on what matters most. Tracking progress here makes your dashboard more actionable and motivating._")
    st.markdown("Set and weight your goals:")
    primary_goal = st.text_input("Primary Goal", key="goals_primary")
    primary_weight = st.slider("Primary Goal Weight", 1, 5, 3, key="goals_primary_weight")
    secondary_goal = st.text_input("Secondary Goal", key="goals_secondary")
    secondary_weight = st.slider("Secondary Goal Weight", 1, 5, 2, key="goals_secondary_weight")
    background_goal = st.text_input("Background Goal", key="goals_background")
    background_weight = st.slider("Background Goal Weight", 1, 5, 1, key="goals_background_weight")
    if st.button("Continue", key="goals_continue"):
        st.session_state['goals'] = {
            'primary': {'goal': primary_goal, 'weight': primary_weight},
            'secondary': {'goal': secondary_goal, 'weight': secondary_weight},
            'background': {'goal': background_goal, 'weight': background_weight}
        }
        go_to('dashboard')
        st.rerun()
        return


def page_dashboard():
    typewriter("# Personal Dashboard Summary\n" + get_greeting() + "\nHere’s a summary of your session:", delay=0.01)
    st.markdown("_Why? Your dashboard brings together your focus, reflections, and goals so you can see patterns, celebrate wins, and spot areas for improvement. Use this as your personal progress map._")
    st.markdown("## Life-Vibe Weights")
    st.bar_chart(pd.DataFrame.from_dict(st.session_state['vibe_weights'], orient='index', columns=['Weight']))
    st.markdown("## Reflection")
    st.write(st.session_state['reflection'])
    st.markdown("## Goals")
    for tier, g in st.session_state['goals'].items():
        st.markdown(f"{tier.capitalize()}: {g['goal']} (Weight: {g['weight']}/5)")
    if st.button("Finish & See Big Pitch"):
        go_to('big_pitch')
        st.rerun()
        return
    st.info("If you do not see the pitch after clicking, please scroll to the top of the page.")
    st.stop()


def page_big_pitch():
    # ...existing code for scroll-to-top script and typewriter...
    # Force scroll to top so typewriter text is always visible
    st.markdown("""
        <script>
            window.parent.scrollTo(0, 0);
            setTimeout(function() {
                window.parent.scrollTo(0, 0);
            }, 150);
        </script>
    """, unsafe_allow_html=True)
    st.markdown("_Why? The Big Pitch explains the vision behind this tool and how your data and feedback can help shape its future. Read on for inspiration and to see how you’re part of something bigger!_")
    typewriter(
        """# The Big Pitch: Why This Matters

Imagine waking up and actually feeling in sync with your own life - not just chasing tasks, but seeing real progress, catching burnout before it starts, and having a system that adapts to you, not the other way around.

This isn't just another productivity tool. This is about building a real, living feedback loop for your mind, your energy, your goals, and your wellbeing.

**How does it all tie together?**
- Every check-in, reflection, and goal you set feeds into your dashboard, giving you a living map of your progress and patterns.
- The habit tracker, focus sprints, and creativity check-ins aren't just isolated features - they're all connected, so you can see how your energy, mood, and habits influence each other.
- Nudges and micro-tutorials are personalized, triggered by your real data, so you get the right support at the right time.
- The recap and expanded info help you zoom out, spot trends, and make smarter decisions for the week ahead.
- As the community grows, anonymized insights will help everyone see what's working for people like them - turning individual progress into collective wisdom.
- The more you use it, the more powerful it gets: your data, your patterns, your feedback all feed into a smarter, more supportive system for everyone.

**The Data & Insights Arm: Why It's a Game-Changer**
- With user consent, anonymized data can power research into what really helps people avoid burnout, build habits, and stay on track.
- We can surface trends: What habits help most with energy? What reflection prompts lead to the biggest breakthroughs?
- Imagine a dashboard for the whole community: 'This week, people who did X habit saw a 20% boost in mood.'
- This data can be used to create new features, smarter nudges, and even open up partnerships with researchers, wellness orgs, and companies who want to support their people better.
- There's huge value in being able to say: 'Here's what actually works, for real people, in the real world.'
- Long-term, the data arm could become a revenue stream itself - offering anonymized, ethical insights to organizations, or powering new AI-driven tools for users.
- The data also helps us build a feedback loop: the more we learn, the better we can help you (and everyone else) grow.

**What are the real benefits?**
- Spot burnout before it hits: Get early warnings when your energy, mood, or habits start to slip.
- See your progress, not just your to-dos: Visual dashboards and recaps show you how far you've come, not just what's left to do.
- Adapt to real life: The system learns your rhythms - if you're having a rough week, it helps you adjust, not guilt-trip you.
- Build habits that stick: Track, tweak, and celebrate small wins so you actually build momentum.
- Get nudges that matter: Contextual tips and encouragements based on your real data, not generic advice.
- Feel less alone: Community features (coming soon) let you share, learn, and get support from people on the same journey.
- Make better decisions: See patterns in your mood, energy, and focus so you can plan smarter, not harder.
- Save time and mental energy: Automated recaps, reminders, and insights mean less mental clutter and more clarity.
- Use your data for good: Opt in to help power research, new features, and collective breakthroughs.

**The User Journey: From Day One to Year One**
- Day 1: You start with a simple check-in. Maybe you're feeling a bit off, or maybe you're just curious.
- Week 1: You notice patterns - your energy dips on Wednesdays, your mood lifts after creative sprints.
- Month 1: You've built a couple of habits, dodged a burnout spiral, and started using the dashboard to plan your week.
- Month 3: You're part of a challenge group, sharing tips and wins, and you've got a streak going.
- Month 6: You've got a year's worth of insights, and you're helping shape new features with your feedback.
- Year 1: You look back and see real, measurable growth - not just in your goals, but in your resilience, your self-awareness, and your ability to adapt.

**The Business & Impact Vision**
1. Quick Revenue Streams:
    - Early supporter memberships: For a few pounds a month, get access to new features, community, and direct input into the roadmap.
    - Pay-what-you-want upgrades: Unlock custom dashboards, extra analytics, or AI-powered nudges for whatever you think it's worth.
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
3. Why It's Built to Succeed:
    - No big team, no burn rate: My own skills and passion are always free to the project. I'll handle the tech, content, and groundwork myself for the first few months - so there's no pressure to chase funding or rack up costs.
    - Fast iteration: We can experiment, launch, and adapt quickly, based on real user feedback - not just guesses.
    - Community-first: Every feature is designed to help people help each other, not just themselves.
    - Real impact: The more people use it, the more valuable the insights and support become - for everyone.
    - Data-driven: The more we learn, the more we can help - every user, every organization, every new feature.

**The Future We Can Build**
Picture this: A year from now, thousands of people are using this system to stay on track, avoid burnout, and actually enjoy the process of growth. They're sharing what works, supporting each other, and building a movement around self-awareness and sustainable progress.

The project is self-sustaining, with a steady stream of revenue from people who genuinely value what it offers. There's no pressure to sell out, no need to chase investors or ads. Just a growing, thriving community - and the freedom to keep making it better, together.

If you're reading this, you're not just a user - you're a co-creator. Your feedback, your ideas, and your energy are what will make this work.

Let's build something that actually makes a difference. Let's make self-reflection, progress tracking, and real support the new normal.
""", delay=0.002)

    st.markdown("---")
    st.markdown("### Have questions or feedback?")
    user_feedback = st.text_area("Ask anything or share your thoughts (optional):", key="user_feedback")
    if user_feedback:
        st.success("Thank you for your feedback! We'll use it to improve the tool.")
page = st.session_state.get('page', 'personalisation')
if page == 'personalisation':
    page_personalisation()
elif page == 'life_vibe':
    page_life_vibe()
elif page == 'reflection':
    page_reflection()
elif page == 'goals':
    page_goals()
elif page == 'dashboard':
    page_dashboard()
elif page == 'big_pitch':
    page_big_pitch()
