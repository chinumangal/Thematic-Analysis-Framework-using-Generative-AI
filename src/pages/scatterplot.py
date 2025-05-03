import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import os

# Load data (Replace with your actual file path)
local_dir = os.path.abspath(os.path.join(__file__, "../../../data/"))
embeddings_path =  os.path.join(local_dir, "output_embeddings4.csv")
df = pd.read_csv(embeddings_path)  # Ensure this has 'Domain' and 'Embedding'

fieldname = '1.1 Domain'
keywords_field = f"Keywords_{fieldname}"
field_embeddings = f"embeddings_Keywords_{fieldname}"


# Convert string embeddings to numpy arrays (if stored as strings in CSV)
df['Embedding'] = df[field_embeddings].apply(lambda x: np.array(eval(x)) if isinstance(x, str) else np.array(x))

# Stack embeddings into a matrix
X = np.vstack(df['Embedding'].values)

# Apply PCA to reduce dimensions to 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

# Convert PCA output to DataFrame
df_pca = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
df_pca['Domain'] = df[keywords_field]

# Plot PCA scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x="PC1", y="PC2", hue="Domain", data=df_pca, palette="tab10", s=100)
plt.title("PCA Scatter Plot of Domain Similarities")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")

# Add labels for better readability
for i, row in df_pca.iterrows():
    plt.text(row["PC1"], row["PC2"], row["Domain"], fontsize=9, ha="right")

plt.show()
