"""
02_image_generation.py
Modul Demonstrasi Image Generation (Latent Diffusion Sampling, Prompt Parsing & ControlNet)
"""

import time
import math

def parse_prompt_conditioning(prompt: str, negative_prompt: str) -> dict:
    """Membedah text prompt menjadi token embedding conditioning vektor."""
    print(f"📝 Prompt Positif : '{prompt}'")
    print(f"🚫 Prompt Negatif : '{negative_prompt}'")
    
    # Tokenization simulation
    positive_tokens = prompt.lower().split()
    negative_tokens = negative_prompt.lower().split()
    
    return {
        "text_encoder": "CLIP ViT-L/14 + OpenCLIP ViT-H",
        "guidance_scale (CFG)": 7.5,
        "positive_token_count": len(positive_tokens),
        "negative_token_count": len(negative_tokens)
    }

def simulate_diffusion_sampling_loop(steps: int = 5, cfg_scale: float = 7.5):
    """Simulasi proses Denoising Loop pada Latent Diffusion Model (e.g. Stable Diffusion / DALL-E)."""
    print(f"\n🎨 Memulai Reverse Diffusion Process ({steps} Sampling Steps, CFG={cfg_scale}):")
    print("   [Step 0] Latent Space filled with pure Gaussian Noise N(0, I)")
    
    for i in range(1, steps + 1):
        noise_level = (steps - i) / steps
        signal_to_noise = math.log(i + 1) * 2.5
        print(f"   [Step {i}/{steps}] Denoising... Noise Level: {noise_level:.2f} | SNR: {signal_to_noise:.2f} dB")
        time.sleep(0.05)
        
    print("   ✨ Latent Space Denoised! Passing through VAE Decoder to RGB Pixel Space...")
    print("   🖼️ Canvas Rendered: [1024 x 1024 PNG, 24-bit Color]")

def simulate_controlnet_conditioning(edge_map_type: str = "Canny"):
    """Simulasi pengontrolan struktur visual menggunakan ControlNet."""
    print(f"\n📐 [ControlNet Conditioning] Menggunakan structural guide: {edge_map_type}")
    print("   1. Ekstraksi Edge Map dari input reference image.")
    print("   2. Menyuntikkan fitur spatial ke residual blocks U-Net encoder.")
    print("   3. Menjaga pose / komposisi objek sesuai panduan Canny Edge.")

def main():
    print("=" * 70)
    print("🎨 MODUL 02: IMAGE GENERATION (LATENT DIFFUSION & CONTROLNET)")
    print("=" * 70)

    # 1. Prompt Conditioning
    conditioning = parse_prompt_conditioning(
        prompt="Cyberpunk futuristic city at night, neon lights, highly detailed 8k cinematic photo",
        negative_prompt="blurry, low quality, distorted text, ugly"
    )
    print("\nText Conditioning Parameters:")
    for k, v in conditioning.items():
        print(f"  • {k}: {v}")

    # 2. Diffusion Sampling
    simulate_diffusion_sampling_loop(steps=5, cfg_scale=7.5)

    # 3. ControlNet
    simulate_controlnet_conditioning(edge_map_type="Canny Edge Detection")

    print("\n✅ Modul Image Generation Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
