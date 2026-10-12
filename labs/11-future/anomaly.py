"""Optional ML lab: synthetic data; requires numpy and scikit-learn."""
import numpy as np
from sklearn.ensemble import IsolationForest

random = np.random.default_rng(42)
normal = np.column_stack([random.poisson(2, 300), random.uniform(0, 0.8, 300)])
model = IsolationForest(n_estimators=120, contamination=0.03, random_state=42)
model.fit(normal)

cases = [('ordinary', 2, 0.2), ('denied-spike', 28, 0.3), ('rpc-spike', 2, 9.0)]
for name, denied, errors in cases:
    predicted = model.predict([[denied, errors]])[0] == -1
    print(f'{name}: flagged_for_review={predicted}')
print('No case here represents a confirmed cyberattack.')
