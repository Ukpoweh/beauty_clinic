import psycopg2
import streamlit as st
from datetime import datetime

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="beauty_clinic",
        user="postgres",
        password="UKPOWEH22"
    )
    return conn


def add_client(username, first_name, last_name, phone, email):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Insert client information
        cursor.execute("""
            INSERT INTO Clients (username, first_name, last_name, phone, email) 
            VALUES (%s, %s, %s, %s, %s)
        """, (username, first_name, last_name, phone, email))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success(f"Client profile added successfully! Your Username is: {username}")
    except psycopg2.errors.UniqueViolation:
        st.error("Username already exists. Please choose a different username.")
    except Exception as e:
        st.error(f"Error: {e}")

def main():
    st.title("Beauty Clinic Management System")
    st.sidebar.title("Menu")
    st.sidebar.markdown("Choose an option from the sidebar.")
    
    if st.button("Add Client"):
        st.subheader("Add Client")
        username = st.text_input("Username")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")

        if st.button("Submit"):
            if username and first_name and last_name and phone and email:
                add_client(username, first_name, last_name, phone, email)
            else:
                st.error("Please fill in all required fields.")


if __name__ == "__main__":
    main()

