# Data dictionary

All seeded rows use `source_type = synthetic_pilot`. They are simulated for method demonstration and should not be described as human-subject data.

Key variables:
- `loneliness_score`: custom 7-item loneliness battery scaled 0-100.
- `social_connection_score`: custom 6-item connection/support battery scaled 0-100.
- `immediate_reward_bias`: percentage of delay-choice tasks where the immediate reward was selected.
- `impulsive_spending_score`: custom 5-item spending impulse battery scaled 0-100.
- `high_risk_choice_score`: percentage of risk tasks where the riskier option was selected.
- `conflict_defense_score`: custom conflict-withdrawal/reactivity task scaled 0-100.
- `risk_decision_index`: weighted composite = 0.35*reward + 0.25*spending + 0.25*risk + 0.15*conflict.
- `top_quartile_risk`: 1 if the risk index is in the sample top quartile.

Recommended next step: collect live survey responses through the website. Those rows are stored as `live_submission` in SQLite and should be exported before inferential claims are made.