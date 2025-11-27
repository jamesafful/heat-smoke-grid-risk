import pandas as pd
import statsmodels.api as sm

def fit_logit_event(df, y_col, x_cols):
    X = sm.add_constant(df[x_cols])
    y = df[y_col]
    model = sm.Logit(y, X, missing="drop").fit(disp=False)
    return model
