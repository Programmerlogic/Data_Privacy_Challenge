# 🔐 Data Privacy Challenge  
### *Unmasking the Private: Adversarial Attacks on Differential Privacy*

---

## 🧪 Test Folder  
Used for training the model.

To get started, simply run:  
```bash
python gui.py
```

---

## ⚙️ Workflow Overview:

1. **Preprocessing**  
   - One-hot encode or normalize both datasets: `df_A` and `df_B`.

2. **Triplet Embedding Training**  
   - Train the model to learn an embedding space where similar rows are placed close together.

3. **Encode Both Datasets**  
   - Transform `df_A` and `df_B` into the learned embedding space.

4. **Matching Using FAISS**  
   - Find the top-1 nearest neighbor for each row.  
   - Record both the distances and corresponding indices.

5. **Scoring & Filtering**  
   - Convert distances into confidence scores using:  
     `confidence = 1 / (1 + distance)`

6. **Evaluation**  
   - Results are stored in `matched_results.csv`  
     - `index_y`, `name_y`: refer to the **original.csv**  
     - `index_x`, `name_x`: refer to the **challenge.csv**

---

## 📊 Evaluation Metrics

- **Approximate Accuracy** *(no duplicate A-IDs)*: `99.53%`  
- **Mean Match Confidence**: `0.9867`  
- **Confidence-Weighted Accuracy**: `98.21%`  
- **Matches with Confidence ≥ 0.8**: `99.00%`  

---

## 📷 Visual Insights  

![Triplet Loss Visualization](https://github.com/user-attachments/assets/0fd4099e-4877-4170-bcd0-f8df5328fe37)

![Confidence Distribution](https://github.com/user-attachments/assets/908a3eb4-dcf9-47b6-9b01-4fcdef46571d)

