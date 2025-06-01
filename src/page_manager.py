import streamlit as st

home_page = st.Page("pages/homepage.py", title="Home", icon=":material/home:")
load_data_page = st.Page("pages/load_data.py", title="Load Data", icon=":material/upload:")
domain_page = st.Page("pages/1_1_domain.py", title = "Domain" )
use_case_page = st.Page("pages/1_2_use_cases.py", title = "Use Cases" )
data_type_page = st.Page("pages/1_3_data_types.py", title = "Data type" )
implication_page = st.Page("pages/1_4_implications.py", title = "Implications" )
resources_page = st.Page("pages/1_5_resources.py", title = "Learning resources" )
learners_page = st.Page("pages/2_1_learners.py", title = "Learners" )
instructors_page = st.Page("pages/2_2_instructors.py", title = "Instructors" )
internal_support_page = st.Page("pages/2_3_internal_support.py", title = "Internal Support" )
outcomes_page = st.Page("pages/3_1_outcomes.py", title = "Learning Outcomes" )
assessment_page = st.Page("pages/3_2_assessment.py", title = "Assessment" )
activities_page = st.Page("pages/3_3_activities.py", title = "Learning Activities" )


pg = st.navigation([home_page, load_data_page, domain_page, use_case_page, data_type_page, implication_page, learners_page, instructors_page, internal_support_page,  assessment_page, activities_page])
# st.set_page_config(page_title="Data manager", page_icon=":material/edit:")




pg.run()