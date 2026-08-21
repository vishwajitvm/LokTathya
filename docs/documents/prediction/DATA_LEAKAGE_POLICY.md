# Data Leakage Prevention
Data leakage is strictly prohibited. Features must NEVER incorporate information (surveys, demographic shifts, boundary redraws) that occurred *after* the temporal `train_cutoff` date.
Any feature flagged with a `HIGH` lookahead risk in the Feature Registry is automatically rejected.
