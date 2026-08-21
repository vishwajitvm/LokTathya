# Temporal Split (Data Leakage Prevention)
```mermaid
graph TD
    Data[Historical Elections] --> Split[Temporal Backtesting Engine]
    Split --> Train1[Train: <= 2009]
    Split --> Train2[Train: <= 2014]
    Split --> Train3[Train: <= 2019]
    Train1 --> Pred1[Predict: 2014]
    Train2 --> Pred2[Predict: 2019]
    Train3 --> Pred3[Predict: 2024]
```
