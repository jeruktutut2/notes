"""
Modul 03: Supervised Fine-Tuning (SFT)
Skrip 1: Manual PyTorch SFT Training Loop (Causal LM Target Loss)
"""

import torch
import torch.nn as nn
import torch.optim as optim

class SimpleCausalLM(nn.Module):
    """
    Model miniatur Causal Language Model untuk peragaan SFT Training Loop.
    """
    def __init__(self, vocab_size=100, embed_dim=64):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, embed_dim, batch_first=True)
        self.head = nn.Linear(embed_dim, vocab_size)
        
    def forward(self, input_ids):
        x = self.embedding(input_ids)
        out, _ = self.lstm(x)
        logits = self.head(out)
        return logits

def demo_sft_training_loop():
    print("=" * 60)
    print("MODUL 03 - SKRIP 1: Manual SFT Training Loop (PyTorch)")
    print("=" * 60)
    
    vocab_size = 100
    model = SimpleCausalLM(vocab_size=vocab_size)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss(ignore_index=-100)
    
    # Synthetic Batch Data (Batch size=2, Seq len=8)
    # Token 1 s/d 4 adalah Prompt (-100 di label), Token 5 s/d 8 adalah Respon
    input_ids = torch.tensor([
        [10, 11, 12, 13, 20, 21, 22, 23],
        [10, 14, 15, 13, 30, 31, 32, 33]
    ])
    
    labels = torch.tensor([
        [-100, -100, -100, -100, 20, 21, 22, 23],
        [-100, -100, -100, -100, 30, 31, 32, 33]
    ])
    
    print("Melatih model selama 50 epoch miniatur...\n")
    
    for epoch in range(1, 51):
        model.train()
        optimizer.zero_grad()
        
        logits = model(input_ids) # Shape: (Batch, SeqLen, VocabSize)
        
        # Shift logits dan labels untuk Causal Next-Token Prediction
        shift_logits = logits[:, :-1, :].contiguous().view(-1, vocab_size)
        shift_labels = labels[:, 1:].contiguous().view(-1)
        
        loss = criterion(shift_logits, shift_labels)
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0 or epoch == 1:
            print(f"Epoch {epoch:02d} | Cross-Entropy Loss: {loss.item():.4f}")
            
    print("\n[OK] Training Loop SFT Selesai! Loss terkonvergensi menuju angka yang lebih kecil.")

if __name__ == "__main__":
    demo_sft_training_loop()
