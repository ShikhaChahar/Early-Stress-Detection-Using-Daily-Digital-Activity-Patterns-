def build_features(df):
    df = df.copy()

    df["screen_per_session"] = df["screen_time"] / (df["app_sessions"] + 1)
    df["night_screen_ratio"] = df["night_usage"] / (df["screen_time"] + 1)
    df["sleep_deficit"] = 8 - df["sleep_hours"]

    feature_cols = [
        "screen_time", "app_sessions", "night_usage",
        "call_count", "sms_count", "sleep_hours", "app_entropy",
        "screen_per_session", "night_screen_ratio", "sleep_deficit"
    ]

    return df[feature_cols]