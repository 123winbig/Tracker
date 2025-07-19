import streamlit as st
import matplotlib.pyplot as plt
from collections import Counter

# 🎯 Loop numbers and wheel layout
kaprekar = [9, 18, 27, 36]
wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
         10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

# 🧠 Sidebar controls
st.sidebar.header("🔧 Tracker Settings")
starting_bank = st.sidebar.number_input("💰 Starting Bank", min_value=100, max_value=10000, value=300, step=50)
strategy = st.sidebar.selectbox(
    "🎯 Choose Strategy",
    ["Strategy 1: Bet after 10 cold loop spins (1NB)",
     "Strategy 2: Bet after 8 cold loop spins, 1NB hit",
     "Strategy 3: Bet after 5 cold loop spins, 2NB hit"]
)

# 🧠 Session init
if "bank" not in st.session_state:
    st.session_state.bank = starting_bank
    st.session_state.cold_streaks = {num: 0 for num in kaprekar}
    st.session_state.history = []
    st.session_state.bank_history = [starting_bank]

def get_neighbors(num, n=1):
    idx = wheel.index(num)
    return [wheel[(idx - i) % len(wheel)] for i in range(1, n + 1)] + \
           [wheel[(idx + i) % len(wheel)] for i in range(1, n + 1)]

def reset_session():
    st.session_state.bank = starting_bank
    st.session_state.cold_streaks = {num: 0 for num in kaprekar}
    st.session_state.history = []
    st.session_state.bank_history = [starting_bank]
    st.success(f"🔄 Reset complete! Starting bank: €{starting_bank}")

def update(spin):
    st.session_state.history.append(spin)
    win = False
    total_bet = 0
    instructions = []

    for loop in kaprekar:
        st.session_state.cold_streaks[loop] += 1
        bet_size = 1

        loop_hit = spin == loop
        neighbors_1 = get_neighbors(loop, n=1)
        neighbors_2 = get_neighbors(loop, n=2)

        if loop_hit:
            st.session_state.cold_streaks[loop] = 0

        should_bet = False
        targets = []

        if strategy.startswith("Strategy 1") and st.session_state.cold_streaks[loop] >= 10:
            targets = [loop] + neighbors_1
            should_bet = True
        elif strategy.startswith("Strategy 2") and st.session_state.cold_streaks[loop] >= 8 and spin in neighbors_1:
            targets = [loop] + neighbors_1
            should_bet = True
        elif strategy.startswith("Strategy 3") and st.session_state.cold_streaks[loop] >= 5 and spin in neighbors_2 and spin not in neighbors_1:
            targets = [loop] + neighbors_2
            should_bet = True

        if should_bet:
            instructions.append((loop, st.session_state.cold_streaks[loop], bet_size, targets))
            total_bet += bet_size * len(targets)
            if spin in targets:
                win = True
                st.session_state.bank += bet_size * 35
                st.session_state.cold_streaks[loop] = 0

    st.session_state.bank -= total_bet
    st.session_state.bank_history.append(st.session_state.bank)
    return instructions, total_bet, win

# 🖥️ Main layout
st.set_page_config(page_title="Roulette Command Center", layout="centered")
st.title("🎰 Unified Roulette Tracker")

if st.button("🔄 Reset Session"):
    reset_session()

spin = st.number_input("Enter Spin Result (0–36)", min_value=0, max_value=36, step=1)
if st.button("Run Spin"):
    instructions, total_bet, win = update(spin)
    st.subheader("📌 Betting Instructions")
    for row in instructions:
        st.write(f"✅ Bet | Loop {row[0]} | Cold Streak: {row[1]} | Targets: {row[3]}")
    st.write(f"💰 Total Bet: €{total_bet}")
    st.write(f"🏦 Bank After Spin: €{st.session_state.bank}")
    st.write(f"✅ Win: {'Yes' if win else 'No'}")

if st.session_state.bank_history:
    st.subheader("📈 Bank Balance Over Spins")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.bank_history, marker='o', color='green')
    ax.set_xlabel("Spin #")
    ax.set_ylabel("Bank (€)")
    ax.grid(True)
    st.pyplot(fig)

if st.session_state.history:
    st.subheader("📋 Session Summary")
    st.write(f"Total Spins: {len(st.session_state.history)}")
    st.write(f"Final Bank: €{st.session_state.bank}")
    st.write(f"Highest Bank: €{max(st.session_state.bank_history)}")
    st.write(f"Lowest Bank: €{min(st.session_state.bank_history)}")

if len(st.session_state.history) >= 50:
    st.subheader("🔥 Hot & ❄️ Cold Numbers (Last 50 Spins)")
    recent = st.session_state.history[-50:]
    hot = Counter(recent).most_common(5)
    cold = [n for n in range(37) if n not in recent]
    st.markdown("**🔥 Hot Numbers:**")
    for n, c in hot:
        st.write(f"Number {n} → {c} hits")
    st.markdown("**❄️ Cold Numbers:**")
    st.write(cold)
