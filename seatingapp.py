import streamlit as st
import pandas as pd
from telegram import Bot
import os

st.set_page_config(page_title="GITD Recognition Dinner 2024", page_icon="🍽")

# Load the data from the Excel file
data_path = "List of Table Number_07122024.xlsx"

def load_data(path):
    df = pd.read_excel(path)
    return df

# Main app function
def run_main():
    # Load data
    df = load_data(data_path)
    df['STAFF ID'] = df['STAFF ID'].astype(str)
    staff_id_list = df['STAFF ID'].tolist()
    staff_id_list_lowcase = [item.lower() for item in staff_id_list]

    # Main app layout
    st.markdown(
        """
        <style>
        /* General styling */
        .main {
            background-color: #f9f9f9;
            padding: 2rem;
            font-family: 'Segoe UI', sans-serif;
        }
        .centered-content {
            max-width: 600px;
            margin: 0 auto;
        }
        .header {
            font-size: 2.5rem;
            font-weight: 600;
            color: #2c3e50;
            text-align: center;
        }
        .sub-header {
            font-size: 1rem;
            color: #7f8c8d;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .input-label {
            font-size: 1rem;
            color: #34495e;
            font-weight: 500;
        }
        .success {
            font-size: 1.1rem;
            color: #2e7d32;
            margin-top: 1rem;
        }
        .error {
            font-size: 1.1rem;
            color: #d32f2f;
            margin-top: 1rem;
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #95a5a6;
            margin-top: 3rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Header Section
    st.info("Interns, please check with the committee for your seat number.", icon="ℹ️")
    # st.markdown("<div class='header'>Welcome to</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Welcome to</div>", unsafe_allow_html=True)
    st.image("gitd_dinner_logo.png", use_container_width=True)

    # Input Section
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    staff_id = st.text_input("Enter your Staff ID to find your seats:", label_visibility="visible").strip()
    staff_id_lowcase = staff_id.lower()

    # col1, col2, col3 = st.columns(3)

    # with col2:
    # Validation and Output
    if st.button("Confirm Attendance"):
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        CHAT_ID = os.getenv('CHAT_ID')
        if staff_id:
            if staff_id_lowcase not in staff_id_list_lowcase:
                st.markdown("<div class='error'>🚫 Staff ID not found! Please try again, or contact the organizer.</div>", unsafe_allow_html=True)
            else:
                employee = df.loc[df['STAFF ID'].str.lower() == staff_id_lowcase, 'EMPLOYEE'].values[0]
                table_no = df.loc[df['STAFF ID'].str.lower() == staff_id_lowcase, 'TABLE NO'].values[0]
                division = df.loc[df['STAFF ID'].str.lower() == staff_id_lowcase, 'DIV'].values[0]

                if pd.isna(table_no): ### NOT UPDATED
                    st.warning(f"Dear **{employee}**, your seating number is not assigned yet. Please contact the organizer")
                
                elif isinstance(table_no, str) and "-" in table_no: ### NORMAL ATTENDEES
                    st.markdown(
                        f"<div class='success'>🎉 Welcome <strong>{employee}</strong> ({division})! You can seat anywhere between the table <strong>{table_no}</strong></div>", 
                        unsafe_allow_html=True
                    )

                    bot = Bot(token=BOT_TOKEN)
                    bot.send_message(chat_id=CHAT_ID, text=f"{staff_id}, {employee}, {division}, {table_no}")
                
                elif isinstance(table_no, str) and "Committee" in table_no: ### COMMITTEE
                    st.markdown(
                        f"<div class='success'>🎉 Welcome <strong>{employee}</strong> ({division})! You may proceed to the <strong>committee</strong> table</div>", 
                        unsafe_allow_html=True
                    )

                    bot = Bot(token=BOT_TOKEN)
                    bot.send_message(chat_id=CHAT_ID, text=f"{staff_id}, {employee}, {division}, {table_no}")

                elif isinstance(table_no, str) and "VIP" in table_no: ### VIP
                    st.markdown(
                        f"<div class='success'>🎉 Welcome <strong>{employee}</strong> ({division})! You may proceed to the <strong>VIP</strong> table</div>", 
                        unsafe_allow_html=True
                    )

                    bot = Bot(token=BOT_TOKEN)
                    bot.send_message(chat_id=CHAT_ID, text=f"{staff_id}, {employee}, {division}, {table_no}")

                else: ### AWARD RECIPIENTS
                    st.markdown(
                        f"<div class='success'>🎉 Welcome <strong>{employee}</strong> ({division})! Your dedicated table number is: <strong>{table_no}</strong></div>", 
                        unsafe_allow_html=True
                    )

                    bot = Bot(token=BOT_TOKEN)
                    bot.send_message(chat_id=CHAT_ID, text=f"{staff_id}, {employee}, {division}, {table_no}")
        else:
            pass
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer Section
    st.markdown("""
        <style>
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: gray;
        }
        </style>
        <div class='footer'>Powered by Streamlit | Organized by GITD</div>
        """,
        unsafe_allow_html=True,
    )
# Run the app
run_main()
