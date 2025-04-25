# Data_Privacy_Challenge
Unmasking the Private: Adversarial Attacks on Differential Privacy<br>
**Test Folder** is used for the purpose of training the model<br>
Run the **gui.py** file<br>
**WorkFlow**<br>
->1. Preprocessing<br>
One-hot encode or normalize both data sets (df_A and df_B)<br>
->2. Triplet Embedding Training<br>
Train to learn an embedding space such that similar rows are near each other<br>
->3. Code Both Datasets<br>
->4. Matching to FAISS<br>
Get top-1 (or top-K) nearest neighbors for each row<br>
Measure distances and indices<br>
->5. Score and Filter<br>
Transform distances into confidence: confidence = 1 / (1 + distance).<br>
->7. Evaluate **[In matched_results.csv the index_y,name_y is index and name respectively of original.csv and index_x,name_x is index and name respectively of challenge.csv]**
<br>
![0aa88b9b-ac58-4683-8fe0-c26dc9c319e6](https://github.com/user-attachments/assets/0fd4099e-4877-4170-bcd0-f8df5328fe37)

![1df5f9a1-c16f-41a0-808d-e83aa5c3ffe8](https://github.com/user-attachments/assets/908a3eb4-dcf9-47b6-9b01-4fcdef46571d)

**Evaluation Metrics**<br>
Approximate Accuracy (no duplicate A-IDs): 99.53%<br>
Mean Match Confidence: 0.9867<br>
Confidence-Weighted Accuracy: 98.21%<br>
Matches with Confidence ≥ 0.8: 99.00%<br>
