-- preview data 
SELECT *
FROM patients
limit 5;

-- show doctor who has an exps more than 5 year
SELECT doctor_id, first_name, last_name, specialization, years_experience
FROM doctors
WHERE years_experience > 5
ORDER BY years_experience DESC;

-- modify table
-- join table 
-- show patient name and doctor name make appointment
SELECT p.first_name AS patient_name, d.first_name AS doctor_name, a.appointment_date
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id 
JOIN doctors d ON a.doctor_id = d.doctor_id
ORDER BY a.appointment_date;

-- same
-- SELECT p.first_name AS patient_name, d.first_name AS doctor_name, a.appointment_date
-- FROM appointments a, patients p, doctors d
-- WHERE a.patient_id = p.patient_id 
-- AND a.doctor_id = d.doctor_id
-- ORDER BY a.appointment_date;

-- summarize how many times, each appointment for each type and total cost for each type
SELECT treatment_type, COUNT(*) AS treatment_count, SUM(cost) AS total_cost
FROM treatments
GROUP BY treatment_type
ORDER BY total_cost DESC;

-- find insight
-- revenue for the month(include treatment from billing)
SELECT strftime('%Y-%m', bill_date) AS billing_month,
		sum(amount) AS total_revenue
FROM billing
GROUP BY billing_month
ORDER BY billing_month;

-- total revenue from each doctor
SELECT d.first_name ||' '|| d.last_name AS doctor_name, SUM(b.amount) AS revenue, d.specialization
FROM billing b
JOIN treatments t ON b.treatment_id = t.treatment_id
JOIN appointments a ON t.appointment_id = a.appointment_id
JOIN doctors d ON a.doctor_id = d.doctor_id
GROUP BY doctor_name
ORDER BY revenue DESC;

-- patient who has the most appointment
SELECT p.first_name ||' '|| p.last_name AS patient_name,
		count(*) AS total_appointments
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
GROUP BY patient_name
ORDER BY total_appointments DESC;
-- if we not use groupby in SQLite its will random select row and count evary appointment

-- for patient who did appointment but not showing up (missing)
SELECT p.first_name ||' '|| p.last_name AS patient_name,
		count(*) AS missed
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
WHERE status = 'No-show'
GROUP BY patient_name
ORDER BY missed DESC;

-- KPI: Income per doctor and time of appointment
SELECT d.first_name ||' '|| d.last_name AS doctor_name,
	sum(b.amount) AS total_income,
	count(DISTINCT a.appointment_id) AS number_appointment,
	d.specialization
FROM appointments a 
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN treatments t ON a.appointment_id = t.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY doctor_name
ORDER BY total_income DESC;

-- view for income per month
DROP VIEW IF EXISTS monthly_income;
CREATE VIEW monthly_income AS
SELECT strftime('%Y-%m', bill_date) AS month,
		sum(amount) AS total_amount
FROM billing
GROUP BY month;

SELECT *
FROM monthly_income;

-- view for doctor KPI
DROP VIEW IF EXISTS doctors_kpi;
CREATE VIEW doctors_kpi AS
SELECT d.first_name ||' '|| d.last_name AS doctor_name,
	sum(b.amount) AS total_income,
	count(DISTINCT a.appointment_id) AS number_appointment,
	d.specialization
FROM appointments a 
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN treatments t ON a.appointment_id = t.appointment_id
JOIN billing b ON t.treatment_id = b.treatment_id
GROUP BY doctor_name
ORDER BY total_income DESC;

SELECT *
FROM doctors_kpi;