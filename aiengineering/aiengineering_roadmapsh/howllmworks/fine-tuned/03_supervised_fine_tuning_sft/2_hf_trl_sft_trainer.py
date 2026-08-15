"""
Modul 03: Supervised Fine-Tuning (SFT)
Skrip 2: Integration Hugging Face `trl` SFTTrainer & TrainingArguments
"""

def demo_trl_sft_trainer():
    print("=" * 60)
    print("MODUL 03 - SKRIP 2: Hugging Face `trl` SFTTrainer Setup")
    print("=" * 60)
    
    try:
        from trl import SFTTrainer, SFTConfig
        from datasets import Dataset
        from transformers import AutoModelForCausalLM, AutoTokenizer
        
        print("\n--- 1. Menyiapkan Dataset Sintetis ---")
        data = {
            "text": [
                "<|im_start|>user\nApa itu fine-tuning?<|im_end|>\n<|im_start|>assistant\nFine-tuning adalah proses penyesuaian bobot LLM pada dataset spesifik.<|im_end|>",
                "<|im_start|>user\nSebutkan jenis PEFT!<|im_end|>\n<|im_start|>assistant\nJenis PEFT meliputi LoRA, QLoRA, Prefix Tuning, dan Prompt Tuning.<|im_end|>"
            ]
        }
        dataset = Dataset.from_dict(data)
        print(f"Dataset berhasil dibuat dengan {len(dataset)} baris teks.")
        
        print("\n--- 2. Menyiapkan SFTConfig (TRL v0.8+) ---")
        sft_config = SFTConfig(
            dataset_text_field="text",
            max_seq_length=256,
            output_dir="./results_sft",
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            logging_steps=1,
            num_train_epochs=1,
            fp16=False,
            save_strategy="no"
        )
        print(f"Config Output Dir : {sft_config.output_dir}")
        print(f"Learning Rate     : {sft_config.learning_rate}")
        print(f"Batch Size Effective : {sft_config.per_device_train_batch_size * sft_config.gradient_accumulation_steps}")
        
        print("\n[OK] Struktur SFTTrainer & SFTConfig tervalidasi dengan baik!")
        
    except ImportError:
        print("[INFO] Package 'trl' atau 'transformers' belum terinstall secara penuh. Menampilkan contoh skrip standar:")
        print("""
        from trl import SFTTrainer, SFTConfig
        
        sft_config = SFTConfig(
            dataset_text_field="text",
            max_seq_length=512,
            output_dir="./outputs",
            learning_rate=2e-4,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=2,
            num_train_epochs=3,
        )
        
        trainer = SFTTrainer(
            model=model,
            train_dataset=dataset,
            peft_config=peft_config,
            args=sft_config
        )
        trainer.train()
        """)

if __name__ == "__main__":
    demo_trl_sft_trainer()
