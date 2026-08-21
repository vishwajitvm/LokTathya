# Backtesting & Temporal Splits
Random Train/Test splits (e.g., `scikit-learn` `train_test_split`) are BANNED for election data. 
All evaluations MUST utilize the `BacktestingEngine` expanding-window temporal split (e.g., Train <= 2014, Predict 2019).
