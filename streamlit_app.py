import streamlit as st
import matplotlib.pyplot as plt

kaprekar = [9, 18, 27, 36]
wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23,
         10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

if "bank" not in st.session_state:
    st.session_state.bank = 300
    st.session_state.cold_streaks = {num: 0 for num in kaprekar}
    st.session_state.history = []
    st.session_state.bank_history = []

def get_neighbors(num, n=2):
    idx = wheel.index(num)
    return [wheel[(idx - i) % len(wheel)] for i in range(1, n+1)] + \
           [wheel[(idx + i) % len(wheel)] for i in range(1, n+1)]

def reset_session():
    st.session_state.bank = 300
    st.session_state.cold_streaks = {num: 0 for num in kaprekar}
    st.session_state.history = []
    st.session_state.bank_history = []
    st.success("🔄 Session reset!")

def update(spin):
    st.session_state.history.append(spin)
    win = False
    total_bet = 0
    instructions = []

    for num in kaprekar:
        st.session_state.cold_streaks[num] += 1
        bet_size = 1 if st.session_state.cold_streaks[num] < 10 else 2 if st.session_state.cold_streaks[num] < 20 else 3 if st.session_state.cold_streaks[num] < 30 else 4
        neighbors = get_neighbors(num)
        targets = [num] + neighbors

        if st.session_state.cold_streaks[num] >= 2:
            instructions.append((num, st.session_state.cold_streaks[num], bet_size, targets))
            total_bet += bet_size * len(targets)

        if spin in targets:
            win = True
            st.session_state.bank += bet_size * 35
            st.session_state.cold_streaks[num] = 0

    st.session_state.bank -= total_bet
    st.session_state.bank_history.append(st.session_state.bank)

    return instructions, total_bet, win

# 🎰 UI Layout
st.set_page_config(page_title="Roulette Tracker", layout="centered")
st.title("🎰 Dynamic Roulette Tracker")

if st.button("🔄 Reset Session"):
    reset_session()

spin = st.number_input("Enter Spin Result (0–36)", min_value=0, max_value=36, step=1)
if st.button("Run Spin"):
    instructions, total_bet, win = update(spin)
    st.subheader("📌 Betting Instructions")
    for row in instructions:
        st.write(f"Loop {row[0]} | Cold Streak: {row[1]} | Bet Size: {row[2]} | Targets: {row[3]}")
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
