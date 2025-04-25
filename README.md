# Data_Privacy_Challenge
Unmasking the Private: Adversarial Attacks on Differential Privacy

WorkFlow
->1. Preprocessing<br>
One-hot encode or normalize both data sets (df_A and df_B)
->2. Triplet Embedding Training
Train to learn an embedding space such that similar rows are near each other
->3. Code Both Datasets
->4. Matching to FAISS
Get top-1 (or top-K) nearest neighbors for each row
Measure distances and indices
->5. Score and Filter
Transform distances into confidence: confidence = 1 / (1 + distance).
->7. Evaluate

![0aa88b9b-ac58-4683-8fe0-c26dc9c319e6](https://github.com/user-attachments/assets/0fd4099e-4877-4170-bcd0-f8df5328fe37)

![1df5f9a1-c16f-41a0-808d-e83aa5c3ffe8](https://github.com/user-attachments/assets/908a3eb4-dcf9-47b6-9b01-4fcdef46571d)

Approximate Accuracy (no duplicate A-IDs): 99.53%
Mean Match Confidence: 0.9867
Confidence-Weighted Accuracy: 98.21%
Matches with Confidence ≥ 0.8: 99.00%
