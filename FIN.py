import streamlit as st
import math
import random

st.set_page_config(page_title="Financial Intelligence System", layout="wide")

st.title("💰 Advanced Financial Intelligence System")

# ---------------- SESSION STATE FIX ----------------
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

# ---------------- FORMAT ----------------
def format_inr(n):
    if n >= 1e7:
        return f"₹{n/1e7:.2f} Cr"
    elif n >= 1e5:
        return f"₹{n/1e5:.2f} Lakh"
    elif n >= 1e3:
        return f"₹{n/1e3:.2f} K"
    return f"₹{n:.0f}"

# ---------------- INPUT ----------------
st.header("📥 Inputs")

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Monthly Income", min_value=0)
    emi = st.number_input("Monthly EMI", min_value=0)
    expenses = st.number_input("Monthly Expenses", min_value=0)

with col2:
    loan_amount = st.number_input("Total Loan Taken", min_value=0)
    loan_rate = st.number_input("Loan Interest Rate (%)", value=6.0)
    emi_years = st.number_input("EMI Years Left", min_value=1, value=5)

lump_sum = st.number_input("Lump Sum Savings", min_value=0)

# ---------------- BUTTON ----------------
if st.button("🚀 Analyze"):
    st.session_state.analyzed = True

# ---------------- MAIN LOGIC ----------------
if st.session_state.analyzed:

    if income == 0 or emi == 0 or expenses == 0:
        st.error("Income, EMI, Expenses cannot be zero")
        st.stop()

    # ---------------- CORE CALCULATIONS ----------------
    savings = income - emi - expenses
    monthly_cashflow = savings

    # ---------------- LOAN BURDEN ----------------
    st.header("🏦 Loan Burden Analysis")

    rate = loan_rate / 100
    years = emi_years

    interest = loan_amount * rate * years
    loan_burden = loan_amount + interest
    emi_burden = emi * 12 * years
    total_burden = loan_burden + emi_burden

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Loan Burden")
        st.write(f"Loan Taken: {format_inr(loan_amount)}")
        st.write(f"Interest ({years} yrs): {format_inr(interest)}")
        st.write(f"Total Loan: {format_inr(loan_burden)}")

    with col2:
        st.subheader("EMI Burden")
        st.write(f"Monthly EMI: {format_inr(emi)}")
        st.write(f"Total EMI Paid: {format_inr(emi_burden)}")

    with col3:
        st.subheader("Total Burden")
        st.write(f"Total Payable: {format_inr(total_burden)}")

    # ---------------- LUMP SUM STRATEGY ----------------
    st.header("🏦 Lump Sum Strategy")

    emergency = emi * 6
    investable = max(lump_sum - emergency, 0)

    st.write(f"Emergency Fund (6 months EMI): {format_inr(emergency)}")
    st.write(f"Investable Amount: {format_inr(investable)}")

    col1, col2 = st.columns(2)

    # FD
    with col1:
        st.subheader("🏦 FD / Bank")
        st.caption("No Risk (Safe Return)")

        if investable > 0:
            fd_rate = 0.06
            fd_years = 5
            fd_value = investable * ((1 + fd_rate) ** fd_years)

            st.write(f"Investable Amount: {format_inr(investable)}")
            st.write(f"Interest Rate: 6%")
            st.write(f"Duration: 5 Years")
            st.success(f"Final Amount: {format_inr(fd_value)}")

    # SIP (Lump sum growth)
    with col2:
        st.subheader("📈 SIP Investment")
        st.caption("Risky but Higher Returns")

        if investable > 0:
            sip_rate = 0.10
            sip_value = investable * ((1 + sip_rate) ** 5)

            st.write(f"Investable Amount: {format_inr(investable)}")
            st.write(f"Interest Rate: 10%")
            st.write(f"Duration: 5 Years")
            st.success(f"Final Amount: {format_inr(sip_value)}")

    # ---------------- SAVINGS SECTION ----------------
    st.header("💵 Monthly Savings Strategy")

    if savings <= 0:
        st.error("You have to save money for your future ⚠️")
    else:
        st.success(f"Your Monthly Savings: {format_inr(savings)}")

        # ---------------- SIP SLIDER ----------------
        st.subheader("📊 Smart SIP Planner (Adjust & See Growth)")

        col1, col2, col3 = st.columns(3)

        with col1:
            sip_amount = st.slider("Monthly Investment (₹)", 1000, 50000, 10000, step=1000)

        with col2:
            sip_years = st.slider("Investment Duration (Years)", 1, 30, 10)

        with col3:
            sip_rate = st.slider("Expected Return (%)", 5, 20, 12)

        months = sip_years * 12
        monthly_rate = sip_rate / 12 / 100

        future_value = sip_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        total_invested = sip_amount * months
        profit = future_value - total_invested

        st.subheader("💰 Your Investment Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Total Invested", format_inr(total_invested))

        with c2:
            st.metric("Wealth Gained", format_inr(profit))

        with c3:
            st.metric("Future Value", format_inr(future_value))


        if sip_amount < 5000:
            st.error("🚨 Low investment → Wealth creation will be slow.")
        elif sip_amount < 15000:
            st.warning("⚠️ Good start, but increase SIP for faster financial freedom.")
        else:
            st.success("🔥 Strong investing habit! You are building real wealth.")


        # ---------------- YOUR ADDED SIP PLANS ----------------
        st.subheader("📈 SIP Plans (Long Term - Low Risk)")

        r = 0.12
        years = 20
        n = years * 12

        def sip_future(monthly):
            return monthly * (((1 + r/12)**n - 1) / (r/12)) * (1 + r/12)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("₹5K SIP Plan")
            val = sip_future(5000)
            st.write("Monthly Investment: ₹5,000")
            st.write("Interest Rate: 12%")
            st.write("Investment Period: 20 Years")
            st.success(f"Final Amount: {format_inr(val)}")

        with col2:
            st.subheader("₹10K SIP Plan")
            val = sip_future(10000)
            st.write("Monthly Investment: ₹10,000")
            st.write("Interest Rate: 12%")
            st.write("Investment Period: 20 Years")
            st.success(f"Final Amount: {format_inr(val)}")

        with col3:
            st.subheader("₹20K SIP Plan")
            val = sip_future(20000)
            st.write("Monthly Investment: ₹20,000")
            st.write("Interest Rate: 12%")
            st.write("Investment Period: 20 Years")
            st.success(f"Final Amount: {format_inr(val)}")

    # ---------------- CASHFLOW ----------------
    st.header("💸 Monthly Cashflow")

    st.metric("Monthly Savings", format_inr(monthly_cashflow))

    if monthly_cashflow < 0:
        st.error("Negative cashflow ⚠️")
    else:
        st.success("Positive cashflow 👍")

    # ---------------- MOTIVATION ----------------
    st.success(random.choice([
        "Discipline + Time = Wealth",
        "SIP is slow but powerful 🚀",
        "High EMI reduces your freedom, not just your money.",
        "You are one step away from a debt trap",
        "Control your EMI before it controls your life.",
        "Be careful today, or regret tomorrow",
        "Your future depends on what you reduce now.",
        "Loans buy comfort today but cost freedom tomorrow.",
        "Not all EMIs are bad, but too many are dangerous.",
        "Assets make you rich, liabilities make you busy.",
        "If your money isn't growing, your problems are.",
        "Financial stress is not income problem, it's habit problem."
    ]))