* Loneliness and Risk Decisions - Stata-ready analysis script
clear all
set more off
import delimited "data/synthetic_participants.csv", clear

* Reliability checks
alpha lq1-lq7
alpha sci1-sci6

* Standardized predictors
egen loneliness_z = std(loneliness_score)
egen social_connection_z = std(social_connection_score)
egen stress_z = std(self_reported_stress_0_100)
egen age_z = std(age)
egen platform_sessions_z = std(platform_sessions_per_day)
egen sleep_z = std(sleep_hours)
gen loneliness_x_connection = loneliness_z * social_connection_z

* Core OLS model
reg risk_decision_index loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection, robust

* Logistic model for top quartile risk profile
logit top_quartile_risk loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection
estat classification

* Group comparison
oneway risk_decision_index loneliness_group, tabulate

* Outcome-specific models
foreach y in immediate_reward_bias impulsive_spending_score high_risk_choice_score conflict_defense_score {
    reg `y' loneliness_z social_connection_z stress_z age_z platform_sessions_z sleep_z loneliness_x_connection, robust
}
