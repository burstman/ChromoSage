import streamlit as st
conn = st.experimental_connection('gather_db', type='sql')

# View the connection contents.
conn