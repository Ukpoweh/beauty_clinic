import psycopg2
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
import pandas as pd 

def connect_db():
    conn = psycopg2.connect(
        host="database-1.ctoc8qcc6ldb.eu-north-1.rds.amazonaws.com",  # RDS endpoint
        database="beautyClinic",
        user="postgres",
        password="UKPOWEH22",
        port=5432
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



def is_valid_username(username):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "SELECT COUNT(*) FROM Clients WHERE Username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()[0]
        return result > 0  # Returns True if the username exists, False otherwise
    finally:
        cursor.close()
        conn.close()


def get_services():
    conn = connect_db()
    services = pd.read_sql("SELECT serviceid, servicetype FROM Services", conn)
    conn.close()
    return services


def schedule_appointment(username, date, service_type, status="Scheduled"):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Appointments (Username, Date, ServiceID, Status) 
            VALUES (%s, %s, %s, %s)
        """, (username, date, service_type, status))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Appointment scheduled successfully!")
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown('''
<style>
body {
background-image: url("https://marynassifchbat.com/wp-content/uploads/2018/11/9W8A0273-11-853x853.jpg");
background-size: cover;
}
</style>
''', unsafe_allow_html=True)

def main():
   
    with st.sidebar:
        selected = option_menu(
            menu_title= "Main Menu",
            options=["Home", "Create your customer profile", "Schedule an Appointment"],
            default_index=0,
            menu_icon="cast",

        )
    if selected=="Create your customer profile":
        with st.form("client_form"):
            st.subheader("Create your customer profile")
            username = st.text_input("Username")
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            phone = st.text_input("Phone Number")
            email = st.text_input("Email Address")

            submitted = st.form_submit_button("Create")

            if submitted:
                if username and first_name and last_name and phone and email:
                    add_client(username, first_name, last_name, phone, email)
                else:
                    st.error("Please fill in all required fields.")


    if selected=="Schedule an Appointment":
        with st.form("appointment_form"):
            st.subheader("Schedule an Appointment")
            username = st.text_input("Username")
            col1, col2 = st.columns([1,1])
            with col1:
                date = st.date_input("Appointment Date")
            with col2:
                time = st.time_input("Appointment Time", step=3600)

            appointment_datetime = datetime.combine(date, time)
            services = get_services()

            #st.write("Available Services:", services)
    
            # Dropdown to select a service
            service_dict = dict(zip(services["servicetype"], services["serviceid"]))
            selected_service = st.selectbox("Service Type", options=list(service_dict.keys()))

            # Convert service name to ID
            service_id = service_dict[selected_service]

            submitted = st.form_submit_button("Click to Schedule")

            if submitted:
                if not username or not date or not service_id:
                    st.error("Please fill in all required fields.")
                else:
                    if is_valid_username(username):
                        schedule_appointment(username, appointment_datetime, service_id)
                    else:
                        st.error("The username entered does not exist. Please ensure you enter the exact username you used when creating your client profile.")
                

if __name__ == "__main__":
    main()

