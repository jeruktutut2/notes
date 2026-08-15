"""
03_chatbot_arena_elo.py
-----------------------
Simulasi LMSYS Chatbot Arena ELO Rating System:
1. Perhitungan Expected Win Probability
2. Pembaruan Skor ELO berbasis Pertandingan Pairwise (Win / Loss / Tie)
3. Papan Peringkat (Leaderboard Generation)
"""

class ChatbotArenaElo:
    def __init__(self, initial_rating: float = 1000.0, k_factor: float = 32.0):
        self.initial_rating = initial_rating
        self.k_factor = k_factor
        self.ratings = {}

    def get_rating(self, model_name: str) -> float:
        """Mengambil rating model saat ini (default 1000 jika baru)."""
        return self.ratings.get(model_name, self.initial_rating)

    def calculate_expected_score(self, rating_a: float, rating_b: float) -> float:
        """Menhitung probabilitas Model A menang melawan Model B."""
        return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))

    def record_match(self, model_a: str, model_b: str, result: str) -> dict:
        """
        Merekam satu pertandingan antara Model A vs Model B.
        result: "A_win", "B_win", atau "Tie"
        """
        r_a = self.get_rating(model_a)
        r_b = self.get_rating(model_b)

        e_a = self.calculate_expected_score(r_a, r_b)
        e_b = self.calculate_expected_score(r_b, r_a)

        if result == "A_win":
            s_a, s_b = 1.0, 0.0
        elif result == "B_win":
            s_a, s_b = 0.0, 1.0
        else: # Tie
            s_a, s_b = 0.5, 0.5

        # Update rating ELO
        new_r_a = r_a + self.k_factor * (s_a - e_a)
        new_r_b = r_b + self.k_factor * (s_b - e_b)

        self.ratings[model_a] = round(new_r_a, 1)
        self.ratings[model_b] = round(new_r_b, 1)

        return {
            "model_a": model_a,
            "old_r_a": round(r_a, 1),
            "new_r_a": round(new_r_a, 1),
            "model_b": model_b,
            "old_r_b": round(r_b, 1),
            "new_r_b": round(new_r_b, 1),
            "result": result
        }

    def get_leaderboard(self) -> list[dict]:
        """Menghasilkan papan peringkat model dari rating tertinggi."""
        sorted_models = sorted(self.ratings.items(), key=lambda x: x[1], reverse=True)
        return [
            {"rank": idx + 1, "model": model, "elo_rating": rating}
            for idx, (model, rating) in enumerate(sorted_models)
        ]


if __name__ == "__main__":
    print("=== LAB 09: CHATBOT ARENA ELO RATING SYSTEM ===")

    arena = ChatbotArenaElo()

    # Tournament Simulations
    matches = [
        ("GPT-4o", "Llama-3-8B", "A_win"),
        ("Claude-3.5-Sonnet", "GPT-4o", "Tie"),
        ("Claude-3.5-Sonnet", "Llama-3-8B", "A_win"),
        ("Mistral-7B", "Llama-3-8B", "B_win"),
        ("GPT-4o", "Mistral-7B", "A_win"),
        ("Claude-3.5-Sonnet", "Gemini-1.5-Pro", "A_win"),
        ("Gemini-1.5-Pro", "GPT-4o", "B_win")
    ]

    print("\n[Processing Arena Matches...]")
    for m in matches:
        res = arena.record_match(m[0], m[1], m[2])
        print(f" Match: {m[0]} vs {m[1]} -> Outcome: {m[2]} | New Elo: [{m[0]}: {res['new_r_a']}, {m[1]}: {res['new_r_b']}]")

    print("\n🏆 CHATBOT ARENA LEADERBOARD 🏆")
    print("-" * 45)
    print(f"{'Rank':<6}{'Model Name':<25}{'Elo Rating':<10}")
    print("-" * 45)
    for entry in arena.get_leaderboard():
        print(f"#{entry['rank']:<5}{entry['model']:<25}{entry['elo_rating']:<10}")
    print("-" * 45)
