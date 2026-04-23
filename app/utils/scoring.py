def calculate_opportunity(volume, difficulty, visible):
    volume_score = min(volume / 5000, 1)
    difficulty_score = 1 - (difficulty / 100)
    visibility_score = 1 if not visible else 0.3

    return round(
        (0.5 * volume_score) +
        (0.3 * difficulty_score) +
        (0.2 * visibility_score),
        3
    )