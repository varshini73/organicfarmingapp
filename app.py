import streamlit as st
import sqlite3
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
    conn.commit()
    conn.close()


def authenticate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user


def main():
    st.set_page_config(page_title="Organic Farming Assistant", page_icon="🌱", layout="wide")
    create_user_table()

    menu = ["Home", "Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.markdown("""
        <h1 style='text-align: center; color: green;'>🌿 Organic Farming Assistant 🌿</h1>
        <p style='text-align: center;'>Helping farmers transition to organic farming!</p>
        """, unsafe_allow_html=True)

    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                dashboard()
            else:
                st.error("Invalid Username or Password")

    elif choice == "Sign Up":
        st.subheader("Create a New Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type='password')
        if st.button("Sign Up"):
            add_user(new_user, new_password)
            st.success("Account Created Successfully! You can now log in.")


def dashboard():
    st.sidebar.title("Dashboard")
    options = ["Organic Farming Guide", "Sell Produce", "Market Prices", "Logout"]
    choice = st.sidebar.radio("Go To", options)

    if choice == "Organic Farming Guide":
        st.subheader("📖 Organic Farming Guide")
        st.write("Learn about best practices, certifications, and sustainability techniques.")

    elif choice == "Sell Produce":
        st.subheader("🛒 Sell Your Produce")
        st.write("Connect with buyers and list your organic products.")

    elif choice == "Market Prices":
        st.subheader("📈 Check Market Prices")
        st.write("Stay updated with the latest organic produce prices.")

    elif choice == "Logout":
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.success("Logged out successfully!")


if __name__ == "__main__":
    main()