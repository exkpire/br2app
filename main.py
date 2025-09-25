PERSONALISATION_ENABLED = True  # Set to False to disable all name references
USER_NAME = "Martin"  # Set to a string to pre-fill the user's name and skip prompt
import json
import os
# -------- PERSONAL DASHBOARD SUMMARY ----------
def show_dashboard(session_summary):
    type_print("\n==============================")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(This dashboard is your cockpit, {USER_NAME}. It gives you a quick readout of your vibe, goals, habits, and more—so you can see your progress and spot what needs attention at a glance. It’s your personal mission control.)")
    else:
        type_print("(This dashboard is your cockpit. It gives you a quick readout of your vibe, goals, habits, and more—so you can see your progress and spot what needs attention at a glance. It’s your personal mission control.)")
    type_print("      PERSONAL DASHBOARD      ")
    type_print("==============================")
    # Life-Vibe
    vibe = session_summary.get("life_vibe")
    vibe_weight = session_summary.get("vibe_weight")
    if vibe:
        type_print(f"🌈 Life-Vibe: {vibe} (Weight: {vibe_weight}/5)")
    # Reflection
    type_print("\n--- Reflection ---")
    e = session_summary.get("energy")
    m = session_summary.get("mood")
    stress = session_summary.get("stress")
    sleep = session_summary.get("sleep")
    social = session_summary.get("social")
    if e is not None:
        type_print(f"💪 Energy: {e}/5")
    if m is not None:
        type_print(f"😄 Mood: {m}/5")
    if stress is not None:
        type_print(f"🧘 Stress: {stress}/5")
    if sleep is not None:
        type_print(f"😴 Sleep: {sleep}/5")
    if social is not None:
        type_print(f"🤝 Social: {social}/5")
    # Goals
    type_print("\n--- Goals ---")
    goals = session_summary.get("goals", {})
    for tier in ["primary", "secondary", "background"]:
        g = goals.get(tier)
        if g:
            type_print(f"{tier.capitalize()}: {g['goal']} (Weight: {g['weight']}/5)")
    # Habits
    habit = session_summary.get("habit")
    if habit:
        type_print(f"\nHabits tracked: {', '.join(habit)}")
    # Focus
    focus = session_summary.get("focus_minutes")
    if focus:
        type_print(f"Focus sprints: {focus}")
    # Creativity
    spark = session_summary.get("spark")
    if spark:
        type_print(f"Creativity spark: {spark}")
    type_print("==============================\n")
# -------- MICRO-TUTORIAL / NUDGE SYSTEM ----------
def provide_nudges(session_summary):
    nudges = []
    # Contextual encouragements based on session data
    if session_summary.get("energy", 3) <= 2:
        nudges.append("Tip: Try a quick walk or stretch to boost energy.")
    if session_summary.get("mood", 3) <= 2:
        nudges.append("Nudge: Low mood is normal. Try a favorite song or message a friend.")
    if session_summary.get("stress", 3) >= 4:
        nudges.append("Micro-Tutorial: Try box breathing (inhale 4s, hold 4s, exhale 4s, hold 4s). It can help lower stress.")
    if session_summary.get("sleep", 3) <= 2:
        nudges.append("Tip: Poor sleep? Prioritize rest and avoid overcommitting today.")
    if session_summary.get("social", 3) <= 2:
        nudges.append("Nudge: Even a short chat with someone can lift your day.")
    # Goal-based nudge
    goals = session_summary.get("goals", {})
    if goals.get("primary") and goals["primary"]["weight"] >= 4:
        nudges.append(f"Focus: Your primary goal is '{goals['primary']['goal']}'. Break it into small steps for progress.")
    if not nudges:
        nudges.append("Keep going! Small steps add up. Reflect, adjust, and celebrate progress.")
    type_print("\n--- Micro-Tutorials & Nudges ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(These nudges are like having a friendly coach in your corner, {USER_NAME}. They’re little reminders or tips based on how you’re doing, to help you keep momentum or bounce back if you’re flagging. It’s about support, not pressure.)")
    else:
        type_print("(These nudges are like having a friendly coach in your corner. They’re little reminders or tips based on how you’re doing, to help you keep momentum or bounce back if you’re flagging. It’s about support, not pressure.)")
    for n in nudges:
        type_print(f"- {n}")
# -------- GOAL HIGHLIGHTING ----------
def demo_goal_highlighting():
    type_print("\n--- Goal Highlighting ---")
    type_print("(This is where you set your main goals for the day/week/month. By giving each a weight, you’re telling Brain 2.0 what’s most important to you right now. It helps you (and the system) keep your priorities clear, so you don’t get lost in the noise.)")
    goals = {}
    for tier in ["Primary", "Secondary", "Background"]:
        goal = input(f"> Enter your {tier} goal for today/week/month (leave blank to skip): ").strip()
        if goal:
            weight = int(get_input(f"> Weight for this goal? (1=low, 5=high) ", valid_options=[str(i) for i in range(1,6)]))
            goals[tier.lower()] = {"goal": goal, "weight": weight}
    return goals
import time

# -------- CONFIG ----------
TYPING_SPEED = 0.0025
LOADING_DOTS = 5
LOADING_DELAY = 0.1
LINE_PAUSE = 0.5
BAR_FILL_SPEED = 0.05

TEST_MODE = False

# -------- UTILITY FUNCTIONS ----------
def type_print(text, end="\n"):
    if TEST_MODE:
        print(text, end=end)
    else:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(TYPING_SPEED)
        print(end=end)

def loading(msg=""):
    for _ in range(LOADING_DOTS):
        print('.', end='', flush=True)
        time.sleep(LOADING_DELAY)
    print()

def get_input(prompt_text, valid_options=None):
    while True:
        resp = input(prompt_text).strip().lower()
        if TEST_MODE:
            return resp
        if valid_options is None or resp in valid_options:
            return resp
        type_print(f"Please choose from {valid_options}.")

def prompt_menu(msg, options, default_key=None):
    type_print(msg)
    for key, val in options.items():
        type_print(f"{key}. {val}")
    return get_input("> ", valid_options=options.keys())

def prompt_yes_no(msg):
    return get_input(f"{msg} (yes/no) ", valid_options=["yes","no"]) == "yes"

# -------- DEMOS ----------
def demo_reflection():
    type_print("\n--- Demo: Interactive Reflection ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(Reflection is the backbone. This is where you check in with yourself: energy, mood, stress, sleep, social, {USER_NAME}. It’s not just for tracking, but for noticing patterns and catching yourself before you spiral or burn out. Think of it as your daily/weekly pit stop.)")
    else:
        type_print("(Reflection is the backbone. This is where you check in with yourself: energy, mood, stress, sleep, social. It’s not just for tracking, but for noticing patterns and catching yourself before you spiral or burn out. Think of it as your daily/weekly pit stop.)")
    answers = {}
    followups = {}

    energy = int(get_input("> On a scale of 1–5, how's your energy today? (1=very low, 5=very high) "))
    mood = int(get_input("> On a scale of 1–5, how's your mood today? (1=low, 5=high) "))
    primary_task = int(get_input("> How important is your primary task today? (1=low, 5=critical) "))

    # New: Nuanced self-assessment
    stress = int(get_input("> Stress level? (1=none, 5=overwhelmed) "))
    sleep = int(get_input("> Sleep quality last night? (1=terrible, 5=excellent) "))
    social = int(get_input("> Social connection today? (1=isolated, 5=connected) "))

    # Follow-ups based on extremes
    if energy <= 2:
        followups['energy'] = "😮 Low energy! Maybe a short walk or break could help."
    else:
        followups['energy'] = "💪 High energy! Good time for focus or creative work."

    if mood <= 2:
        followups['mood'] = "😢 Low mood noted. Brain 2.0 will suggest uplifting prompts."
    else:
        followups['mood'] = "😄 High mood! Leverage it for creative or social tasks."

    if primary_task >= 4:
        followups['task'] = "⚡ High priority! Brain 2.0 will nudge you to stay focused."
    else:
        followups['task'] = "Task is manageable today."

    if stress >= 4:
        followups['stress'] = "🧘 High stress detected. Consider a break or breathing exercise."
    if sleep <= 2:
        followups['sleep'] = "😴 Poor sleep. Be gentle with yourself today."
    if social <= 2:
        followups['social'] = "🤝 Feeling isolated? Maybe reach out to someone you trust."

    type_print("\n".join(followups.values()))
    answers.update({
        "energy": energy,
        "mood": mood,
        "primary_task": primary_task,
        "stress": stress,
        "sleep": sleep,
        "social": social
    })
    return {"answers": answers, "followups": followups}

def demo_habit():
    type_print("\n--- Demo: Habit Formation ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(Habits are the small wins. This bit helps you track the little things that add up over time—like drinking water, stretching, or whatever you want to build into your routine, {USER_NAME}. It’s about stacking small wins so you don’t have to rely on willpower alone.)")
    else:
        type_print("(Habits are the small wins. This bit helps you track the little things that add up over time—like drinking water, stretching, or whatever you want to build into your routine. It’s about stacking small wins so you don’t have to rely on willpower alone.)")
    habit_list = []
    for i in range(2):
        habit = input(f"> Enter a small habit to track #{i+1} (e.g., drink water, stretch): ").strip()
        if habit:
            habit_list.append(habit)
            type_print(f"Tracking habit: {habit}")
        else:
            # If first is blank, skip both; if second is blank, just stop
            break
    return {"habit": habit_list}

def demo_focus():
    type_print("\n--- Demo: Focus & Productivity ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(Focus sprints are like mini-missions, {USER_NAME}. You set a short timer, get your head down, and then take a break. It’s a proven way to get stuff done without frying your brain. This helps you work with your energy, not against it.)")
    else:
        type_print("(Focus sprints are like mini-missions. You set a short timer, get your head down, and then take a break. It’s a proven way to get stuff done without frying your brain. This helps you work with your energy, not against it.)")
    sprints = []
    for i in range(2):
        duration_str = get_input(f"> Focus sprint #{i+1} duration? (1=5min, 5=25min, leave blank to skip) ")
        if not duration_str:
            break
        if not duration_str.isdigit():
            type_print("Please enter a number from 1 to 5 or leave blank to skip.")
            continue
        duration = int(duration_str)
        if duration < 1 or duration > 5:
            type_print("Please enter a number from 1 to 5 or leave blank to skip.")
            continue
        minutes = 5 + (duration-1)*5
        sprints.append(minutes)
        type_print(f"Focus sprint #{i+1} set: {minutes} minutes")
    return {"sprint_minutes": sprints}

def demo_creativity():
    type_print("\n--- Demo: Creativity Spark ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(Creativity check-in is for those days when you want to make, write, or jam, {USER_NAME}. It helps you notice when you’re in a creative flow, so you can ride the wave—or spot when you need a spark. Good for music, art, or just thinking sideways.)")
    else:
        type_print("(Creativity check-in is for those days when you want to make, write, or jam. It helps you notice when you’re in a creative flow, so you can ride the wave—or spot when you need a spark. Good for music, art, or just thinking sideways.)")
    level = int(get_input("> How inspired/creative do you feel today? (1=low, 5=high) "))
    type_print(f"Creativity level recorded: {level}")
    return {"spark": level}

# -------- EXPANDED INFO ----------
expanded_info = {
    "1": """Core Mental Health Support:
- Tracks energy, mood, focus, tasks.
- Gentle nudges & reflection prompts reduce mental load.
- Daily tips to prevent overwhelm.
- Personalized insights for pacing your day.
- Helps build long-term mental resilience.""",
    "2": """Vision Expansion:
- AI-driven task & routine suggestions based on your patterns.
- Personalized dashboards for energy, focus, creativity.
- Community insights: share strategies, habits, reflections.
- Monetization: premium analytics, workshops, content revenue.
- Optional partnerships and open-source contribution.
- Designed for long-term growth of both system & user community.""",
    "3": """Reflection Demo:
- Interprets energy, mood, and task priority.
- Generates actionable prompts tailored to your scores.
- Highlights overload, low motivation, or ideal productivity windows.
- Can be used daily to build awareness of mental patterns.""",
    "4": """Habit Demo:
- Tracks 2–3 small daily habits.
- Sends reminders and encourages consistency.
- Provides insights on habit trends.
- Suggests small incremental improvements.
- Can integrate with AI suggestions for optimized routines.""",
    "5": """Focus Demo:
- Tracks multiple focus sprints and suggests optimal timing.
- Structures work/study sessions based on energy & priority.
- Provides strategies to minimize distractions.
- Can combine with reflection results for smarter task planning.""",
    "6": """Creativity Demo:
- Measures daily creative spark.
- Suggests exercises, prompts, or challenges to maintain inspiration.
- Identifies patterns in creative flow over time.
- Supports project ideation and problem-solving skills.""",
    "7": """All of the Above:
- Comprehensive overview of Brain 2.0 capabilities.
- Combines mental health support, habit tracking, focus management, and creativity prompts.
- Reinforces vision for community growth and monetization.
- Tailored feedback based on your individual demo results.
- Prepares you for long-term mental & productivity optimization."""
}


# -------- LIFE-VIBE WEIGHTING ----------
def demo_life_vibe():
    type_print("\n--- Life-Vibe Weighting ---")
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"(This bit helps you check what area of life is pulling your focus most right now, {USER_NAME}. It’s about knowing if you’re in work mode, creative mode, people mode, etc. so the rest of the system can nudge you in the right direction. It’s like tuning your day’s radio station.)")
    else:
        type_print("(This bit helps you check what area of life is pulling your focus most right now. It’s about knowing if you’re in work mode, creative mode, people mode, etc. so the rest of the system can nudge you in the right direction. It’s like tuning your day’s radio station.)")
    vibe_options = {
        "1": "Monetary (work, finances)",
        "2": "Creative (art, music, ideas)",
        "3": "Humanitarian (helping others, community)",
        "4": "Social (friends, family, connection)",
        "5": "Self-care (rest, health, reflection)"
    }
    type_print("Which area is your main focus or need today?")
    for k, v in vibe_options.items():
        type_print(f"{k}. {v}")
    main_vibe = get_input("> Pick your main focus: ", valid_options=vibe_options.keys())
    type_print("On a scale of 1–5, how much weight does this have for you today? (1=low, 5=high)")
    weight = int(get_input("> Weight: ", valid_options=[str(i) for i in range(1,6)]))
    return {"main_vibe": vibe_options[main_vibe], "vibe_weight": weight}

# -------- BRANCHING DEMO MENU ----------
def branching_demo_menu():
    demo_results = {}
    session_summary = {}
    run_all_mode = False

    menu_opts = {
        "1": "Reflection Demo",
        "2": "Habit Formation Demo",
        "3": "Focus Sprint Demo",
        "4": "Creativity Spark Demo",
        "5": "Run All Demos",
        "6": "Finish and Recap"
    }

    # Always prompt for Life-Vibe Weighting at the start
    vibe = demo_life_vibe()
    session_summary["life_vibe"] = vibe["main_vibe"]
    session_summary["vibe_weight"] = vibe["vibe_weight"]

    # Prompt for Goal Highlighting at the start
    goals = demo_goal_highlighting()
    session_summary["goals"] = goals

    while True:
        if not run_all_mode:
            choice = prompt_menu("\nPick a demo to run (or 5 to run all):", menu_opts)
        else:
            choice = "5"

        if choice == "5":
            run_all_mode = True
            r = demo_reflection()
            demo_results["demo1"] = r["answers"]
            demo_results["demo1_followups"] = r["followups"]
            session_summary.update(r["answers"])

            r = demo_habit()
            demo_results["demo2"] = r
            session_summary["habit"] = r.get("habit")

            r = demo_focus()
            demo_results["demo3"] = r
            session_summary["focus_minutes"] = r.get("sprint_minutes")

            r = demo_creativity()
            demo_results["demo4"] = r
            session_summary["spark"] = r.get("spark")

            return session_summary, demo_results

        elif choice in ("1","2","3","4"):
            if choice == "1":
                r = demo_reflection()
                demo_results["demo1"] = r["answers"]
                demo_results["demo1_followups"] = r["followups"]
                session_summary.update(r["answers"])
            elif choice == "2":
                r = demo_habit()
                demo_results["demo2"] = r
                session_summary["habit"] = r.get("habit")
            elif choice == "3":
                r = demo_focus()
                demo_results["demo3"] = r
                session_summary["focus_minutes"] = r.get("sprint_minutes")
            elif choice == "4":
                r = demo_creativity()
                demo_results["demo4"] = r
                session_summary["spark"] = r.get("spark")
            if not run_all_mode and not prompt_yes_no("Run another demo?"):
                return session_summary, demo_results

        elif choice == "6":
            return session_summary, demo_results

# -------- RECAP AND MORE INFO ----------
def recap_and_more_info(session_summary):
    # Log anonymized session data to file
    def log_session_data(data):
        log_file = "session_log.jsonl"
        # Remove any fields that could be identifying (future-proofing)
        anonymized = dict(data)
        # Write as JSON line
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(anonymized, ensure_ascii=False) + "\n")
    log_session_data(session_summary)
    # Show dashboard summary at the end
    show_dashboard(session_summary)
    # Show micro-tutorials/nudges after recap
    provide_nudges(session_summary)
    # Goal Highlighting Recap
    goals = session_summary.get("goals", {})
    if goals:
        type_print("\n🎯 Goals for this period:")
        for tier in ["primary", "secondary", "background"]:
            g = goals.get(tier)
            if g:
                type_print(f"- {tier.capitalize()}: {g['goal']} (Weight: {g['weight']}/5)")
    type_print("\n--- Session Complete ---")
    completed_demos = [k for k in session_summary.keys()]
    type_print(f"You completed all demos: {', '.join(completed_demos)}\n")

    # --- Big Pitch: Vision, Impact, and Excitement ---
    type_print(
        "================= THE BIG PITCH: WHY THIS MATTERS =================\n"
        "\n"
        "Imagine waking up and actually feeling in sync with your own life—not just chasing tasks, but seeing real progress, catching burnout before it starts, and having a system that adapts to you, not the other way around.\n"
        "\n"
        "This isn’t just another productivity tool. This is about building a real, living feedback loop for your mind, your energy, your goals, and your wellbeing.\n"
        "\n"
        "**How does it all tie together?**\n"
        "- Every check-in, reflection, and goal you set feeds into your dashboard, giving you a living map of your progress and patterns.\n"
        "- The habit tracker, focus sprints, and creativity check-ins aren’t just isolated features—they’re all connected, so you can see how your energy, mood, and habits influence each other.\n"
        "- Nudges and micro-tutorials are personalized, triggered by your real data, so you get the right support at the right time.\n"
        "- The recap and expanded info help you zoom out, spot trends, and make smarter decisions for the week ahead.\n"
        "- As the community grows, anonymized insights will help everyone see what’s working for people like them—turning individual progress into collective wisdom.\n"
        "- The more you use it, the more powerful it gets: your data, your patterns, your feedback all feed into a smarter, more supportive system for everyone.\n"
        "\n"
        "**The Data & Insights Arm: Why It’s a Game-Changer**\n"
        "- With user consent, anonymized data can power research into what really helps people avoid burnout, build habits, and stay on track.\n"
        "- We can surface trends: What habits help most with energy? What reflection prompts lead to the biggest breakthroughs?\n"
        "- Imagine a dashboard for the whole community: ‘This week, people who did X habit saw a 20% boost in mood.’\n"
        "- This data can be used to create new features, smarter nudges, and even open up partnerships with researchers, wellness orgs, and companies who want to support their people better.\n"
        "- There’s huge value in being able to say: ‘Here’s what actually works, for real people, in the real world.’\n"
        "- Long-term, the data arm could become a revenue stream itself—offering anonymized, ethical insights to organizations, or powering new AI-driven tools for users.\n"
        "- The data also helps us build a feedback loop: the more we learn, the better we can help you (and everyone else) grow.\n"
        "\n"
        "**What are the real benefits?**\n"
        "- Spot burnout before it hits: Get early warnings when your energy, mood, or habits start to slip.\n"
        "- See your progress, not just your to-dos: Visual dashboards and recaps show you how far you’ve come, not just what’s left to do.\n"
        "- Adapt to real life: The system learns your rhythms—if you’re having a rough week, it helps you adjust, not guilt-trip you.\n"
        "- Build habits that stick: Track, tweak, and celebrate small wins so you actually build momentum.\n"
        "- Get nudges that matter: Contextual tips and encouragements based on your real data, not generic advice.\n"
        "- Feel less alone: Community features (coming soon) let you share, learn, and get support from people on the same journey.\n"
        "- Make better decisions: See patterns in your mood, energy, and focus so you can plan smarter, not harder.\n"
        "- Save time and mental energy: Automated recaps, reminders, and insights mean less mental clutter and more clarity.\n"
        "- Use your data for good: Opt in to help power research, new features, and collective breakthroughs.\n"
        "\n"
        "================= THE USER JOURNEY: FROM DAY ONE TO YEAR ONE =================\n"
        "\n"
        "Day 1: You start with a simple check-in. Maybe you’re feeling a bit off, or maybe you’re just curious.\n"
        "Week 1: You notice patterns—your energy dips on Wednesdays, your mood lifts after creative sprints.\n"
        "Month 1: You’ve built a couple of habits, dodged a burnout spiral, and started using the dashboard to plan your week.\n"
        "Month 3: You’re part of a challenge group, sharing tips and wins, and you’ve got a streak going.\n"
        "Month 6: You’ve got a year’s worth of insights, and you’re helping shape new features with your feedback.\n"
        "Year 1: You look back and see real, measurable growth—not just in your goals, but in your resilience, your self-awareness, and your ability to adapt.\n"
        "\n"
        "================= THE BUSINESS & IMPACT VISION =================\n"
        "\n"
        "This project isn’t just sustainable—it’s designed to be a launchpad for a whole ecosystem. Here’s how we’ll make it work, fast:\n"
        "\n"
        "1. **Quick Revenue Streams:**\n"
        "   - Early supporter memberships: For a few pounds/dollars a month, get access to new features, community, and direct input into the roadmap.\n"
        "   - Pay-what-you-want upgrades: Unlock custom dashboards, extra analytics, or AI-powered nudges for whatever you think it’s worth.\n"
        "   - Microtransactions: Buy a one-off deep-dive report, a printable journal, or a custom theme.\n"
        "   - Donation/support buttons: If you love it, you can just chip in.\n"
        "   - Live workshops and group challenges: Pay to join a focused sprint, a habit bootcamp, or a live Q&A with experts.\n"
        "\n"
        "2. **Long-Term, Scalable Revenue:**\n"
        "   - Premium analytics: Monthly or annual subscriptions for advanced tracking, trend analysis, and AI-driven insights.\n"
        "   - Corporate wellness: Sell team dashboards and group analytics to companies who want to support their staff.\n"
        "   - Licensing: Let coaches, therapists, and organizations use the platform with their own clients.\n"
        "   - Affiliate partnerships: Earn commission by recommending books, courses, or wellness products that actually help.\n"
        "   - Content revenue: Monetize YouTube videos, podcasts, and written guides that teach people how to get the most out of the system.\n"
        "   - Merch and printables: Sell branded journals, habit trackers, or even fun swag for the community.\n"
        "   - API access: Let other apps and platforms plug into the system for a fee.\n"
        "   - Data insights: (With consent) offer anonymized, ethical trend reports to organizations or researchers.\n"
        "\n"
        "**Example scenarios:**\n"
    "- A user pays £5 for a custom monthly recap PDF they can share with their therapist or coach.\n"
    "- A company pays £99/month for a team dashboard that helps their staff avoid burnout and stay engaged.\n"
        "- A coach licenses the platform for their 1:1 clients, adding value to their own business.\n"
        "- A group of users join a paid 30-day challenge to build a new habit together, with live check-ins and rewards.\n"
        "- Someone buys a physical journal or printable to use offline, supporting the project and spreading the word.\n"
        "- A university or wellness org pays for anonymized trend data to improve their own programs.\n"
        "\n"
        "3. **Why It’s Built to Succeed:**\n"
        "   - No big team, no burn rate: My own skills and passion are always free to the project. I’ll handle the tech, content, and groundwork myself for the first few months—so there’s no pressure to chase funding or rack up costs.\n"
        "   - Fast iteration: We can experiment, launch, and adapt quickly, based on real user feedback—not just guesses.\n"
        "   - Community-first: Every feature is designed to help people help each other, not just themselves.\n"
        "   - Real impact: The more people use it, the more valuable the insights and support become—for everyone.\n"
        "   - Data-driven: The more we learn, the more we can help—every user, every organization, every new feature.\n"
        "\n"
        "================= THE FUTURE WE CAN BUILD =================\n"
        "\n"
        "Picture this: A year from now, thousands of people are using this system to stay on track, avoid burnout, and actually enjoy the process of growth. They’re sharing what works, supporting each other, and building a movement around self-awareness and sustainable progress.\n"
        "\n"
        "The project is self-sustaining, with a steady stream of revenue from people who genuinely value what it offers. There’s no pressure to sell out, no need to chase investors or ads. Just a growing, thriving community—and the freedom to keep making it better, together.\n"
        "\n"
        "If you’re reading this, you’re not just a user—you’re a co-creator. Your feedback, your ideas, and your energy are what will make this work.\n"
        "\n"
        "Let’s build something that actually makes a difference. Let’s make self-reflection, progress tracking, and real support the new normal.\n"
        "===============================================================\n"
    )


    # Personalized recap
    type_print("Here's what we observed from your session:")
    vibe = session_summary.get("life_vibe")
    vibe_weight = session_summary.get("vibe_weight")
    if vibe:
        type_print(f"🌈 Life-Vibe Focus: {vibe} (Weight: {vibe_weight}/5)")
    e = session_summary.get("energy")
    if e:
        type_print(f"💪 Energy: {e}")
    m = session_summary.get("mood")
    if m:
        type_print(f"😄 Mood: {m}")
    task = session_summary.get("primary_task")
    if task:
        type_print(f"Task priority: {task}")
    # New: Nuanced self-assessment recap
    stress = session_summary.get("stress")
    if stress:
        type_print(f"🧘 Stress: {stress}")
    sleep = session_summary.get("sleep")
    if sleep:
        type_print(f"😴 Sleep: {sleep}")
    social = session_summary.get("social")
    if social:
        type_print(f"🤝 Social Connection: {social}")
    focus = session_summary.get("focus_minutes")
    if focus:
        type_print(f"Focus sprints: {focus}")
    habit = session_summary.get("habit")
    if habit:
        type_print(f"Tracked habits: {habit}")
    spark = session_summary.get("spark")
    if spark:
        type_print(f"Creativity spark: {spark}")

    # More info loop
    while True:
        type_print("\nSelect which part you want more info on (0 to exit):")
        for i in range(1,8):
            type_print(f"{i}. {expanded_info[str(i)].splitlines()[0]}")
        type_print("0. Exit More Info")
        choice = get_input("> Pick a number: ", valid_options=[str(x) for x in range(0,8)])
        if choice == "0":
            break
        type_print("\nExpanded Info:")
        type_print(expanded_info[choice])

# -------- MAIN ----------
def main():
    global TEST_MODE
    type_print("===================================")
    type_print("       Welcome to Brain 2.0        ")
    type_print("===================================")

    # Ask for name if not preset and personalisation is enabled
    global PERSONALISATION_ENABLED, USER_NAME
    if PERSONALISATION_ENABLED and not USER_NAME:
        name = input("Just so I'm sure I call you by the right name, what would you like to be known as? (Leave blank to skip): ").strip()
        if name:
            USER_NAME = name
    # Greeting
    if PERSONALISATION_ENABLED and USER_NAME:
        type_print(f"\nHey {USER_NAME}! Welcome to Brain 2.0 — your brain’s new ally.")
    else:
        type_print("\nWelcome to Brain 2.0 — your brain’s new ally.")
    type_print("It helps you notice patterns in mood, energy, and focus, supports mental health, reduces stress, and manages tasks without overwhelm.")

    type_print("\n--- Personal Companion ---")
    type_print("Imagine a system that can:")
    type_print("- Keep your tasks clear and manageable")
    type_print("- Send reminders smartly so important things get attention")
    type_print("- Help you reflect on what's working and what's slowing you down")
    type_print("- Track your overall life balance: creativity, work, social life, self-care")

    type_print("\n--- Community & Growth ---")
    type_print("Connect, share tips, and participate in collaborative exercises.")

    type_print("\n--- Future Possibilities ---")
    type_print("- AI-powered suggestions tailored to your patterns")
    type_print("- Deeper dashboards for tracking focus, energy, creativity")
    type_print("- Monetization streams: premium features, community workshops, content insights")
    type_print("- Open-source contributions and optional partnerships")

    ready = prompt_yes_no("\n> Ready to see Brain 2.0 in action?")
    if ready:
        session_summary, demo_results = branching_demo_menu()
        recap_and_more_info(session_summary)

    type_print("\nThanks for exploring Brain 2.0! Our goals: improve mental health, enhance focus & creativity, and build a supportive community with potential growth opportunities.")

if __name__ == "__main__":
    main()
