# Implementasi Point 6: Evaluasi dan Observability

Cara mengevaluasi kualitas output model dan monitoring performa inference di production.

## Daftar File

1. `1_evaluasi_output_model.py`: Metrik evaluasi output model AI — BLEU (translation), ROUGE (summarization), Exact Match, dan evaluasi berbasis model.
2. `2_cost_latency_tracking.py`: Monitoring biaya (cost per token), latensi (latency), dan throughput inference di production.
3. `3_logging_tracing.py`: Teknik logging dan tracing untuk debugging dan monitoring inference pipeline.

## Konsep Kunci

| Aspek | Metrik | Target |
|-------|--------|--------|
| Kualitas | BLEU, ROUGE, accuracy | Task-dependent |
| Latensi | P50, P95, P99 latency | <2s interactive |
| Biaya | Cost per request/token | Budget-dependent |
| Throughput | Requests per second | Sesuai traffic |
| Reliability | Error rate, uptime | >99.9% |
