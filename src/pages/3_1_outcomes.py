import pandas as pd
import plotly.express as px

# Sample dataframe simulating Gemini output: 1 row per outcome with a Bloom level (1–6)
data = {
    'Course_name': ['Radiology', 'Radiology', 'Aerospace Engineering', 'Aerospace Engineering', 'Agriculture', 'Art and Design'],
    'Cluster': ['Medical & Health Sciences', 'Medical & Health Sciences', 'Engineering & Technology; Natural Sciences', 'Engineering & Technology; Natural Sciences', 'Natural Sciences; Applied Sciences & Vocational Fields', 'Design & Creative Arts'],
    'Outcome': [
        'Understand the fundamental concepts of AI in radiology',
        'Discuss ethical implications of AI in radiology',
        'Design and implement AI models for aerospace tasks',
        'Evaluate AI models in aerospace applications',
        'Analyze agricultural data with AI tools',
        'Apply AI-based style transfer techniques'
    ],
    'Bloom_Level': ['Understand', 'Evaluate', 'Create', 'Evaluate', 'Analyze', 'Apply']
}

df = pd.DataFrame(data)

# Map Bloom's Taxonomy to numeric levels
bloom_map = {
    'Remember': 1,
    'Understand': 2,
    'Apply': 3,
    'Analyze': 4,
    'Evaluate': 5,
    'Create': 6
}

df['Bloom_Level_Num'] = df['Bloom_Level'].map(bloom_map)

# One-hot encode the Bloom levels per outcome
bloom_counts = pd.get_dummies(df['Bloom_Level']).join(df[['Cluster']])
bloom_cluster_avg = bloom_counts.groupby('Cluster').sum().reset_index()

# Normalize to percentage of total outcomes in each cluster
bloom_cluster_avg_percent = bloom_cluster_avg.copy()
bloom_cluster_avg_percent.iloc[:, 1:] = bloom_cluster_avg_percent.iloc[:, 1:].div(
    bloom_cluster_avg_percent.iloc[:, 1:].sum(axis=1), axis=0
)

# Melt for Plotly radar chart
bloom_melted = pd.melt(
    bloom_cluster_avg_percent,
    id_vars='Cluster',
    var_name='Bloom_Level',
    value_name='Proportion'
)

# Multiply proportions by 100 for readability
bloom_melted['Proportion'] *= 100

# Plotly Radar Chart
fig = px.line_polar(
    bloom_melted,
    r='Proportion',
    theta='Bloom_Level',
    color='Cluster',
    line_close=True,
    markers=True,
    title='Bloom\'s Taxonomy Profile per Cluster'
)

fig.update_traces(fill='toself')
fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])))
fig.show()
