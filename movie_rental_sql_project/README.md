# Project 1: Investigate a Relational Database: Movie Rental SQL Project
    

# Insight 1. Family Movie Rentals by Category

We want to understand more about the movies that families are watching. The following categories are considered family movies: Animation, Children, Classics, Comedy, Family and Music.

**The query below lists each movie, the film category it is classified in, and the number of times it has been rented out.**

```sql
WITH film_rental_total
AS (SELECT
  film_id,
  COUNT(rental.rental_id) AS total_rental
FROM inventory
JOIN rental
  ON inventory.inventory_id = rental.inventory_id
GROUP BY film_id)

SELECT
  film.title AS film_title,
  category.name AS category,
  film_rental_total.total_rental AS total_rental
FROM film
JOIN film_rental_total
  ON film.film_id = film_rental_total.film_id
JOIN film_category
  ON film.film_id = film_category.film_id
JOIN category
  ON film_category.category_id = category.category_id
WHERE category.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
ORDER BY category, film_title;
 
```



# Insight 2:  Comparing Rental Trend of Two Stores

We want to find out how the two stores compare in their count of rental orders during every month for all the years we have data for. **The query below returns the store ID for the store, the year and month and the number of rental orders each store has fulfilled for that month. Your table should include a column for each of the following: year, month, store ID and count of rental orders fulfilled during that month.**

```sql
/*Create a table with store, staff and rental information */
WITH store_rental
AS (SELECT
  rental.rental_id AS rental_id,
  DATE_TRUNC('month', rental.rental_date) AS rental_date,
  staff.store_id AS store_id
FROM rental
JOIN staff
  ON rental.staff_id = staff.staff_id)

SELECT
  DATE_PART('month', rental_date) AS Rental_month,
  DATE_PART('year', rental_date) AS Rental_year,
  store_id AS Store_id,
  COUNT(rental_id) AS Count_rentals
FROM store_rental
GROUP BY Rental_year,
         Rental_month,
         Store_id
ORDER BY Rental_year, REntal_month, Store_id;
```

# Insight 3:  Monthly Payments of Top 10 Paying Customers

We would like to know who were our top 10 paying customers, how many payments they made on a monthly basis during 2007, and what was the amount of the monthly payments. **The query below is used to capture the customer name, month and year of payment, and total payment amount for each month by these top 10 paying customers**

```sql
/*Aggregate payment to monthly totals by customer in 2007 */
WITH payment2007 AS (
    SELECT customer_id, 
  	SUM(amount) as pay_amount,
		COUNT(payment_id) as pay_countpermon,
		DATE_TRUNC('month', payment_date) AS pay_mon
		FROM payment
	WHERE DATE_PART('year',payment_date) = 2007
	GROUP BY customer_id, pay_mon)  
/*Join with top10 customers */ 
SELECT
		payment2007.pay_mon AS pay_mon,
		CONCAT(customer.first_name,' ',customer.last_name) AS fullname,
		payment2007.pay_countpermon AS pay_countpermon,
		payment2007.pay_amount AS pay_amount
	FROM customer 
	JOIN payment2007
	ON customer.customer_id = payment2007.customer_id
	JOIN (
		SELECT customer_id, SUM(pay_amount) AS year_total
			FROM payment2007
			GROUP BY customer_id
			ORDER BY year_total DESC 
			LIMIT 10
	) topcustomer
	ON customer.customer_id = topcustomer.customer_id
	ORDER BY fullname,pay_mon;
	
	
```

# Insight 4: Change of Monthly Payments of Top 10 Customers

Finally, for each of these top 10 paying customers, we would like to find out the difference across their monthly payments during 2007. The query below compares the payment amounts in each successive month.In addition, we also identify the customer name who paid the most difference in terms of payments.

```sql
/*Aggregate payment to monthly totals by customer in 2007 */
WITH payment2007 AS (
    SELECT customer_id, 
  	SUM(amount) as pay_amount,
		COUNT(payment_id) as pay_countpermon,
		DATE_TRUNC('month', payment_date) AS pay_mon
		FROM payment
	WHERE DATE_PART('year',payment_date) = 2007
	GROUP BY customer_id, pay_mon),  
/*Join with top10 customers */ 
topcustomer AS (
	SELECT
		payment2007.pay_mon AS pay_mon,
		CONCAT(customer.first_name,' ',customer.last_name) AS fullname,
		payment2007.pay_countpermon AS pay_countpermon,
		payment2007.pay_amount AS pay_amount,
		LEAD(payment2007.pay_amount) OVER
			(PARTITION BY payment2007.customer_id ORDER BY payment2007.pay_mon)
			AS lead,
		(LEAD(payment2007.pay_amount) OVER
			(PARTITION BY payment2007.customer_id ORDER BY payment2007.pay_mon)) - payment2007.pay_amount AS dif_lead
	FROM customer 
	JOIN payment2007
	ON customer.customer_id = payment2007.customer_id
	JOIN 
	(
		SELECT customer_id, SUM(pay_amount) AS year_total
			FROM payment2007
			GROUP BY customer_id
			ORDER BY year_total DESC 
			LIMIT 10
	) top10
	ON customer.customer_id = top10.customer_id
	ORDER BY fullname,pay_mon
)
	
SELECT *, 
	CASE
		WHEN topcustomer.dif_lead = (
			SELECT MAX(topcustomer.dif_lead)
				FROM topcustomer
				LIMIT 1
		) THEN 'maxdif'
		ELSE NULL 
		END AS maxdif_flag
FROM topcustomer
ORDER BY fullname,pay_mon;	
```



