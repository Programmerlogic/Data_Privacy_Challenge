# 🔐 Data Privacy Challenge  
### *Unmasking the Private: Adversarial Attacks on Differential Privacy*

---

## 📂 Test Folder  
Used for **training and testing** the model.

## 📂 Result Folder 
Results and Visuals are stored.

####
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

![image](https://github.com/user-attachments/assets/81617c6e-2a1d-4f3e-b7d9-500044ebf3df)

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

- **Approximate Accuracy** : `99.53%`  
- **Mean Match Confidence**: `0.9867`  
- **Confidence-Weighted Accuracy**: `98.21%`  
- **Matches with Confidence ≥ 0.8**: `99.00%`  

---

## 📷 Visual Insights  

![image](https://github.com/user-attachments/assets/d0a169aa-eddb-4dfe-8887-c2daaf9ed937)

![Confidence Distribution](https://github.com/user-attachments/assets/908a3eb4-dcf9-47b6-9b01-4fcdef46571d)

![match_confidence_scatterplot](https://github.com/user-attachments/assets/27d35f5e-6b10-4897-be07-00b857baee5a)



