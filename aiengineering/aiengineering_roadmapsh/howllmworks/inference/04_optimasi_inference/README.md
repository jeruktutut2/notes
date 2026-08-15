# Implementasi Point 4: Optimasi Inference

Teknik-teknik untuk meningkatkan performa inference — lebih cepat, lebih hemat memori, dan lebih efisien biaya.

## Daftar File

1. `1_quantization.py`: Teknik mengurangi presisi bobot model (FP32 → INT8/INT4) untuk menghemat memori dan mempercepat inference.
2. `2_batching_strategies.py`: Strategi mengelompokkan request untuk meningkatkan throughput — static batching, dynamic batching, continuous batching.
3. `3_caching_kv_cache.py`: Mekanisme KV-Cache yang mempercepat autoregressive generation dengan menyimpan key-value dari token sebelumnya.
4. `4_streaming_output.py`: Teknik streaming response token-by-token untuk pengalaman user yang lebih responsif.

## Konsep Kunci

| Teknik | Manfaat | Trade-off |
|--------|---------|-----------|
| Quantization | -50% memori, ~2x lebih cepat | Sedikit penurunan akurasi |
| Batching | +5-10x throughput | Tambahan latensi per request |
| KV-Cache | ~5-10x lebih cepat generation | Membutuhkan memori tambahan |
| Streaming | UX lebih responsif | Kompleksitas implementasi |
