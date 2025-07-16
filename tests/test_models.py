from predictive_model.src.models import build_pipeline

def test_build_pipeline_instance():
    params = {'n_estimators': 5, 'max_depth': 2, 'learning_rate': 0.1}
    pipe = build_pipeline(params)
    # Pipeline has two steps: scaler + xgb
    assert len(pipe.steps) == 2
    assert pipe.named_steps['xgb'].get_params()['n_estimators'] == 5
