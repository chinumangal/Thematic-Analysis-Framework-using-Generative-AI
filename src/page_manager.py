import streamlit as st



home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
load_data_page = st.Page("pages/load_data.py", title="Load Data", icon=":material/upload:")
search_embeddings_page = st.Page("pages/search.py", title="Search framework", icon=":material/search:")
word_cloud_page = st.Page("pages/word_cloud.py", title="Word clouds", icon=":material/cloud:")
domain_page = st.Page("pages/1_1_domain.py", title = "Domain" )
use_case_page = st.Page("pages/1_2_use_cases.py", title = "Use Cases" )
data_type_page = st.Page("pages/1_3_data_types.py", title = "Data type" )
implication_page = st.Page("pages/1_4_ai_implications.py", title = "Implications" )
resources_page = st.Page("pages/1_5_resources.py", title = "Learning resources" )
learners_page = st.Page("pages/2_1_learners.py", title = "Learners" )
internal_support_page = st.Page("pages/2_3_internal_support.py", title = "Internal Support" )

pg = st.navigation([home_page, load_data_page, domain_page, use_case_page, data_type_page, implication_page, resources_page , learners_page, internal_support_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")




pg.run()