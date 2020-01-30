CREATE TABLE postgres.ohcensus (
	pct_white DECIMAL NOT NULL, 
	pct_black_or_aa DECIMAL, 
	pct_asian DECIMAL, 
	pct_hispanic_latino DECIMAL NOT NULL, 
	pct_less_than_high_school DECIMAL, 
	pct_high_school_grad DECIMAL, 
	pct_bach_or_higher DECIMAL, 
	median_income DECIMAL NOT NULL, 
	pct_households_poverty DECIMAL, 
	pct_households_limited_english DECIMAL, 
	index DECIMAL NOT NULL
);
