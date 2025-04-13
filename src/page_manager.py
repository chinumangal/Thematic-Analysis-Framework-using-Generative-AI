import streamlit as st



home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
load_data_page = st.Page("pages/load_data.py", title="Load Data", icon=":material/upload:")
search_embeddings_page = st.Page("pages/search.py", title="Search framework", icon=":material/search:")
word_cloud_page = st.Page("pages/word_cloud.py", title="Word clouds", icon=":material/cloud:")
domain_page = st.Page("pages/domain.py", title = "Domain" )
data_type_page = st.Page("pages/data_pie.py", title = "Data type" )

pg = st.navigation([home_page, load_data_page, search_embeddings_page, word_cloud_page, domain_page, data_type_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")




pg.run()