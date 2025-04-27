# 🔐 Data Privacy Challenge  (Revised)
### *Unmasking the Private: Adversarial Attacks on Differential Privacy*

---

## 📂 Test Folder  
Used for **training and testing** the model.

## 📂 Result Folder 
Results and Visuals are stored.

---
To get started, simply run:  
```bash
python gui.py
```

---

## 🚀 How to Run the Matching Process

1. **Upload `original.csv`**  
   - This file contains the reference dataset (df_B).

2. **Upload `challenge.csv`**  
   - This file contains the anonymized dataset (df_A).

3. **Load Existing Model**  
   - Use the GUI or backend script to load the pre-trained triplet embedding model.

4. **Run Matching**  
   - The system processes both datasets through the model and runs FAISS-based matching.

5. **Store Result**  
   - The matched results will be saved in a folder as `matched_results.csv`.

**GUI Application** 

![image](https://github.com/user-attachments/assets/dd654784-c5e9-460b-abb0-6e5f9acaaa3b)


---

## ⚙️ Workflow Overview

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

- **Accuracy** : `100.00% (20000/20000)`  
- **Mean Match Confidence**: `0.9861`  
- **Confidence-Weighted Accuracy**: `98.61%`  
- **Matches with Confidence ≥ 0.85**: `99.31% (19862 out of 20000)`
- **Suspicious matches (confidence < 0.85):**`0.69% (138 out of 20000)`

---

## 📷 Visual Insights  

![image](https://github.com/user-attachments/assets/d0a169aa-eddb-4dfe-8887-c2daaf9ed937)

![image](https://github.com/user-attachments/assets/13fdf6e8-7b44-463e-a971-7c3bc7a7fb16)


![match_confidence_scatterplot](https://github.com/user-attachments/assets/76fe8ec3-3270-4a7d-a63e-7c79ef194b7c)



---
## 🎥 Working video



https://github.com/user-attachments/assets/bac56752-3fbb-46d4-b03c-ac46c4a2e57d

