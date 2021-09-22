# Please write a few lines about how to train, test and inference using API with dataset
## tune hyperparameter 
- learning_rate: [0.02,0.04,0.06,0.08,0.1]
- colsample_bytree: [ 0.2, 0.4, 0.6, 0.8, 1]
- max_depth: np.arange(1,25)
- n_estimators: np.arange(100,900,100)
- min_child_weight: np.arange(1,10)
