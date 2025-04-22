import streamlit as st



home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
load_data_page = st.Page("pages/load_data.py", title="Load Data", icon=":material/upload:")
search_embeddings_page = st.Page("pages/search.py", title="Search framework", icon=":material/search:")
word_cloud_page = st.Page("pages/word_cloud.py", title="Word clouds", icon=":material/cloud:")
domain_page = st.Page("pages/domain.py", title = "Domain" )
data_type_page = st.Page("pages/data_pie.py", title = "Data type" )
use_case_page = st.Page("pages/use_cases.py", title = "Use Cases" )
implication_page = st.Page("pages/ai_implications.py", title = "Implications" )
resources_page = st.Page("pages/resources.py", title = "Learning resources" )
learners_page = st.Page("pages/learners.py", title = "Learners" )
internal_support_page = st.Page("pages/internal_support.py", title = "Internal Support" )

pg = st.navigation([home_page, load_data_page, search_embeddings_page, word_cloud_page, domain_page, use_case_page, data_type_page, implication_page, resources_page , learners_page, internal_support_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")




pg.run()