import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import torch
import torch.nn as nn
import random
from torch.utils.data import Dataset, DataLoader
import os
import faiss
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time,threading
from tkinter import ttk

class Encoder(nn.Module):
    def __init__(self, input_dim, latent_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Linear(256, latent_dim)
        )

    def forward(self, x):
        return self.net(x)

class TripletTabularDataset(Dataset):
    def __init__(self, X_anchor, X_positive):
        self.X_anchor = torch.tensor(X_anchor, dtype=torch.float32)
        self.X_positive = torch.tensor(X_positive, dtype=torch.float32)
        self.length = self.X_anchor.shape[0]

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        anchor = self.X_anchor[idx]
        positive = self.X_positive[idx]
        neg_idx = random.choice([i for i in range(self.length) if i != idx])
        negative = self.X_positive[neg_idx]
        return anchor, positive, negative

class TripletGUIApp:
    def __init__(self, master):
        self.master = master
        master.title("Encoder Trainer")
        master.geometry("800x500")

        self.sidebar = tk.Frame(master, width=250, bg="#f0f0f0")
       

        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.sidebar, text="Loaded Files", bg="#f0f0f0", font=("Arial", 14, "bold")).pack(pady=10)

        self.original_label = tk.Label(self.sidebar, text="Original: ", bg="#f0f0f0", anchor='w')
        self.original_label.pack(fill='x', padx=10)

        self.challenge_label = tk.Label(self.sidebar, text="Challenge: ", bg="#f0f0f0", anchor='w')
        self.challenge_label.pack(fill='x', padx=10)

        self.model_label = tk.Label(self.sidebar, text="Model: ", bg="#f0f0f0", anchor='w')
        self.model_label.pack(fill='x', padx=10)

        self.main_frame = tk.Frame(master)
        self.main_frame.pack(expand=True, fill='both')

        tk.Label(self.main_frame, text="Data Privacy Cracker", font=("Arial", 16)).pack(pady=20)

        tk.Button(self.main_frame, text="Upload Original.csv", command=self.load_df_A, width=30, height=2).pack(pady=5)
        tk.Button(self.main_frame, text="Upload Challenge.csv", command=self.load_df_B, width=30, height=2).pack(pady=5)
       
        self.train_button = tk.Button(self.main_frame, text="Train New Model", command=self.train_model, state='disabled', width=30, height=2)
        self.train_button.pack(pady=10)

        self.load_button = tk.Button(self.main_frame, text="Load Existing Model", command=self.load_model, state='disabled', width=30, height=2)
        self.load_button.pack(pady=5)

        self.run_button = tk.Button(self.main_frame, text="Run Matching", command=self.run_matching, state='disabled', width=30, height=2)
        self.run_button.pack(pady=10)

        self.progress_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.progress_label.pack(pady=40)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=10)

        self.summary_frame = tk.LabelFrame(self.sidebar, text="Match Accuracy Summary", padx=10, pady=5)

        self.summary_frame.pack(fill="x", pady=(0, 10))
       
        self.match_stats_var = tk.StringVar()
        self.match_stats_label = tk.Label(self.summary_frame, textvariable=self.match_stats_var, justify="left", anchor="w")
        self.match_stats_label.pack(anchor="w")

       
        self.df_A = None
        self.df_B = None
        self.encoder = None
        self.device =  torch.device('cpu')
        self.latent_dim = 300

    def load_df_A(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.df_A = pd.read_csv(path)
            self.original_label.config(text=f"Original:  {os.path.basename(path)}")
            self.enable_buttons_if_ready()

    def load_df_B(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if path:
            self.df_B = pd.read_csv(path)
            self.challenge_label.config(text=f"Challenge:  {os.path.basename(path)}")
            self.enable_buttons_if_ready()

    def enable_buttons_if_ready(self):
        if self.df_A is not None and self.df_B is not None:
            self.train_button.config(state='normal')
            self.load_button.config(state='normal')
            self.run_button.config(state='normal')

    def preprocess(self):
        df_A= self.df_A.drop(['Name', 'Identifier'], axis=1)
       
        categorical_cols = df_A.select_dtypes(include=['object', 'category']).columns.tolist()
        numerical_cols = df_A.select_dtypes(include=['int64', 'float64']).columns.tolist()
   
        if not numerical_cols:
            raise ValueError("No numerical columns found for scaling.")
   
        all_cols = numerical_cols + categorical_cols
        df_A = df_A[all_cols]
        df_B = self.df_B[all_cols]  
   
        df_A = df_A.fillna(0)
        df_B = df_B.fillna(0)
   
        preprocessor = ColumnTransformer([
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])
   
        X_A_enc = preprocessor.fit_transform(self.df_A)
        X_B_enc = preprocessor.transform(self.df_B)
   
        return X_A_enc, X_B_enc


    def train_model(self):
        X_A_enc, X_B_enc = self.preprocess()
        input_dim = X_A_enc.shape[1]
        self.encoder = Encoder(input_dim=input_dim, latent_dim=self.latent_dim).to(self.device)

        dataset = TripletTabularDataset(X_B_enc, X_A_enc)
        loader = DataLoader(dataset, batch_size=64, shuffle=True)

        loss_fn = nn.TripletMarginLoss(margin=0.1)
        optimizer = torch.optim.Adam(self.encoder.parameters(), lr=1e-3)
        num_epochs = 100

        self.progress_label.config(text="Training started...")

        for epoch in range(num_epochs):
            self.encoder.train()
            total_loss = 0
            for anchor, positive, negative in loader:
                anchor, positive, negative = anchor.to(self.device), positive.to(self.device), negative.to(self.device)

                z_anchor = self.encoder(anchor)
                z_positive = self.encoder(positive)
                z_negative = self.encoder(negative)

                loss = loss_fn(z_anchor,z_positive,z_negative)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            percent = int((epoch + 1) / num_epochs * 100)
            self.progress_label.config(text=f"Training... {percent}% - Loss: {total_loss / len(loader):.4f}")
            self.master.update_idletasks()

        torch.save(self.encoder.state_dict(), "triplet_encoder_model.pth")
        self.model_label.config(text="Model:  triplet_encoder_model.pth")
        self.progress_label.config(text="Training completed and model saved!")

    def load_model(self):
        path = filedialog.askopenfilename(filetypes=[("PyTorch model files", "*.pth")])
        if not path:
            return

        try:
            X_A_enc, _ = self.preprocess()
            input_dim = X_A_enc.shape[1]

            self.encoder = Encoder(input_dim=input_dim, latent_dim=self.latent_dim).to(self.device)

            map_location = torch.device('cpu') if not torch.cuda.is_available() else None
            self.encoder.load_state_dict(torch.load(path, map_location=map_location))
            self.encoder.eval()

            self.model_label.config(text=f"Model: {os.path.basename(path)}")
            self.progress_label.config(text=f"Model loaded: {os.path.basename(path)}")
            self.progress_label.config(text="Ready")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model:\n{str(e)}")

    def run_matching(self):
        threading.Thread(target=self._run_matching_logic).start()

    def _run_matching_logic(self):
        try:
            self.progress_label.config(text="Matching started...")
            self.master.update_idletasks()
   
            X_A_enc, X_B_enc = self.preprocess()
           
            with torch.no_grad():
                X_A_tensor = torch.tensor(X_A_enc, dtype=torch.float32).to(self.device)
                X_B_tensor = torch.tensor(X_B_enc, dtype=torch.float32).to(self.device)
   
                Z_A = self.encoder(X_A_tensor).cpu().numpy()
                Z_B = self.encoder(X_B_tensor).cpu().numpy()
   
            faiss_index = faiss.IndexFlatL2(self.latent_dim)
            faiss_index.add(Z_A.astype(np.float32))
            D, indices = faiss_index.search(Z_B.astype(np.float32), k=20000)
   
            match_data = []
            used_A_indices = set()
            epsilon = 1e-6
            for i in range(len(Z_B)):
                for j in range(20000):
                    a_idx = indices[i][j]
                    if a_idx not in used_A_indices:
                        dist = D[i][j]
                        confidence = 1 / (1 + dist)
                        if abs(confidence - 1) < epsilon:
                            continue
                        match_data.append({
                            "B_index": i,
                            "A_index": a_idx,
                            "match_confidence": confidence
                        })
                        used_A_indices.add(a_idx)
                        break
                if i % 100 == 0 or i == len(Z_B) - 1:
                    self.progress_label.config(text=f"Matching... {i+1}/{len(Z_B)}")
                    self.master.update_idletasks()
   
            self.progress_label.config(text="Finalizing and Saving Results...")
            self.master.update_idletasks()
   
            match_df = pd.DataFrame(match_data)
            final_matched = match_df.merge(self.df_B.reset_index(), left_on="B_index", right_index=True)
            final_matched = final_matched.merge(self.df_A[["Identifier", "Name"]].reset_index(), left_on="A_index", right_index=True)
            final_matched = final_matched.rename(columns={
                'A_index': 'Y_index',
                'B_index': 'X_index'
            })
   
            final_matched = final_matched[['index_x','index_y','match_confidence','Identifier_x','Name_x','Identifier_y','Name_y','Age','Occupation','City_Tier','Dependents','Income',
                                    'Rent','Loan_Repayment','Insurance','Groceries','Transport','Eating_Out','Entertainment','Utilities','Healthcare','Education','Miscellaneous']].copy()
   
            save_path = filedialog.askdirectory()
            if save_path:
                final_matched.to_csv(f"{save_path}/matched_results.csv", index=False)
   
                match_df['Match Confidence Range'] = pd.cut(
                    match_df['match_confidence'],
                    bins=np.arange(0, 1.1, 0.1),
                    labels=[f"{int(l*100)}–{int(r*100)}" for l, r in zip(np.arange(0, 1.0, 0.1), np.arange(0.1, 1.1, 0.1))],
                    right=False
                )
   
                result_df = match_df['Match Confidence Range'].value_counts().sort_index().reset_index()
                result_df.columns = ['Match Confidence Range', 'Count']
                result_df['Percentage'] = (result_df['Count'] / result_df['Count'].sum() * 100).round(2)
   
                plt.figure(figsize=(10, 6))
                bars = plt.bar(result_df['Match Confidence Range'], result_df['Count'],
                            color='teal', edgecolor='black')
   
                for bar, pct, cnt in zip(bars, result_df['Percentage'], result_df['Count']):
                    height = bar.get_height()
                    label = f"{pct}% ({cnt})"
                    plt.text(bar.get_x() + bar.get_width()/2, height + 1,
                            label, ha='center', va='bottom', fontsize=9)
   
                plt.title('Match Confidence Distribution')
                plt.xlabel('Match Confidence (%)')
                plt.ylabel('Count')
                plt.xticks(rotation=45)
                plt.grid(axis='y', linestyle='--', alpha=0.6)
                plt.tight_layout()
                plt.savefig(f"{save_path}/match_confidence_distribution.png")
   
            self.progress_label.config(text="Matching completed!")
            self.master.update_idletasks()
            messagebox.showinfo("Completed", "Matching completed and results saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during matching:\n{str(e)}")

        total_B = len(Z_B)
        total_matched = len(match_df)
        match_accuracy = total_matched / total_B
        mean_confidence = match_df['match_confidence'].mean()
        confidence_weighted_acc = (match_df['match_confidence'] ** 2).sum() / total_B

        summary_text = (
            f"Total Matched: {total_matched} / {total_B}\n"
            f"Match Accuracy: {match_accuracy:.2%}\n"
            f"Mean Confidence: {mean_confidence:.4f}\n"
            f"Confidence-Weighted Accuracy: {confidence_weighted_acc:.4f}"
        )
        self.match_stats_var.set(summary_text)



root = tk.Tk()
app = TripletGUIApp(root)
root.mainloop()
