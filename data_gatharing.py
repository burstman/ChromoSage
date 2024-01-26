import streamlit as st
from sqlalchemy import text


# Function to insert data into PostgreSQL
def insert_into_postgres(insert_color, id_colori, couleur, id_type_tissu, numero_de_bain, delta_a, delta_b, delta_h, delta_l, delta_e, target, percent_red, percent_blue, percent_yellow):

    conn = st.connection("gather_db", type="sql")

    # Insert data into main_table
    with conn.session as session:
        sql_expression = text("""
            INSERT INTO gathering (id_colori, couleur, id_type_de_tissu, numero_de_bain, delta_a, delta_b, delta_h, delta_l, delta_e, target)
            VALUES (:id_colori, :couleur, :id_type_de_tissu, :numero_de_bain, :delta_a, :delta_b, :delta_h, :delta_l, :delta_e, :target)
        """)
        session.execute(sql_expression, {
            'id_colori': id_colori,
            'couleur': couleur,
            'id_type_de_tissu': id_type_tissu,
            'numero_de_bain': numero_de_bain,
            'delta_a': delta_a,
            'delta_b': delta_b,
            'delta_h': delta_h,
            'delta_l': delta_l,
            'delta_e': delta_e,
            'target': target,
        })
        session.commit()
    if insert_color:
        with conn.session as s:
            result = s.execute(text(
                'SELECT data_gather_id FROM gathering ORDER BY data_gather_id DESC LIMIT 1'))
            gather_id = result.scalar()
            sql_expression = text("""
                                INSERT INTO color_correction (data_gather_id,percent_red,percent_blue,percent_yellow)
                                VALUES (:data_gather_id, :percent_red, :percent_blue, :percent_yellow)
                                """)
            session.execute(sql_expression, {
                'data_gather_id': gather_id,
                'percent_red': percent_red,
                'percent_blue': percent_blue,
                'percent_yellow': percent_yellow,
            })
            session.commit()


# Main function to run the Streamlit app
def main():
    st.title("Data Gathering App")
    # Default values for color percentages
    percent_red = 0
    percent_blue = 0
    percent_yellow = 0
    # Create a container for the main inputs
    main_container = st.container(border=True,)

    # Place inputs in the main container
    with main_container:
        col1, col2, col3 = st.columns(3)

        with col1:
            id_colori = st.text_input("ID_colori")

        with col2:
            couleur = st.text_input("couleur")

        with col3:
            id_type_tissu = st.text_input("ID_type de tissu")

        col4, col5, col6 = st.columns(3)

        with col4:
            numero_de_bain = st.number_input(
                "Numero_de_Bain", min_value=0, step=1)

        with col5:
            delta_a = st.number_input("Delta(a)", min_value=0.0, step=0.1)

        with col6:
            delta_b = st.number_input("Delta(b)", min_value=0.0, step=0.1)

        col7, col8, col9 = st.columns(3)

        with col7:
            delta_h = st.number_input("Delta(h)", min_value=0.0, step=0.1)

        with col8:
            delta_l = st.number_input("Delta(L)", min_value=0.0, step=0.1)

        with col9:
            delta_e = st.number_input("Delta(E)", min_value=0.0, step=0.1)

        # Dropdown for selecting the target
        targets = [
            "passer_sans_aucune_correction",
            "passer_avec_savonnage_fort",
            "passer_avec_savonnage_faible",
            "passer_avec_savonnage_faibe sans neutralisation",
            "passer_avec_savonnage_fort sans neutralisation",
            "Ne pas passer faire_correction",
            "passer au savonnage et blocker"
        ]
        selected_target = st.selectbox("Select Target", targets)
        insertcolor = False
        # If the selected target is "color_correction", provide sliders for color percentages
        if selected_target == "Ne pas passer faire_correction":
            insertcolor = True
            col10, col11, col12 = st.columns(3)

            with col10:
                percent_red = st.slider("Percentage of Red (%)", 0, 100, 0)

            with col11:
                percent_blue = st.slider("Percentage of Blue (%)", 0, 100, 0)

            with col12:
                percent_yellow = st.slider(
                    "Percentage of Yellow (%)", 0, 100, 0)

            target_value = f"{selected_target} ({percent_blue}% Blue, {percent_red}% Red, {
                percent_yellow}% Yellow"
        else:
            target_value = selected_target

    # Button to gather and save data
    if st.button("Submit"):
        try:
            # Insert data into PostgreSQL
            insert_into_postgres(insertcolor, id_colori, couleur, id_type_tissu, numero_de_bain, delta_a,
                                 delta_b, delta_h, delta_l, delta_e, target_value, percent_red, percent_blue, percent_yellow)

            st.success("Data saved successfully.")
        except Exception as e:
            st.error(f"An error occurred: {e}")


# Run the Streamlit app
if __name__ == "__main__":
    main()
