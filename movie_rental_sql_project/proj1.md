# About 

This file documents all the SQL scripts for Project 1: Investigate a Relational Database 

# Quiz 

## Quiz 1 

1.   Provides the following details: actor's first and last name combined as full_name, film title, film description and length of the movie.

    ```sql
    SELECT CONCAT(first_name,' ',last_name),
    	film.title,
    	film.description, 
        film.length
    	FROM actor
        JOIN film_actor
        ON actor.actor_id = film_actor.actor_id
        JOIN film
        ON film_actor.film_id = film.film_id;
    ```

2.  Write a query that creates a list of actors and movies where the movie length was more than 60 minutes. How many rows are there in this query result?

```sql
SELECT CONCAT(first_name,' ',last_name),
	film.title,
	film.description, 
    film.length
	FROM actor
    JOIN film_actor
    ON actor.actor_id = film_actor.actor_id
    JOIN film
    ON film_actor.film_id = film.film_id
    WHERE film.length > 60;
```

3.  Write a query that captures the actor id, full name of the actor, and counts the number of movies each actor has made. *(HINT: Think about whether you should group by actor id or the full name of the actor.*) Identify the actor who has made the maximum number movies.

```sql
SELECT actor.actor_id,
	CONCAT(first_name,' ',last_name),
	COUNT(film.film_id) AS film_count
	FROM actor
    JOIN film_actor
    ON actor.actor_id = film_actor.actor_id
    JOIN film
    ON film_actor.film_id = film.film_id
    GROUP BY actor.actor_id
    ORDER BY film_count DESC;
```

## Quiz 2

1.  Write a query that displays a table with 4 columns: actor's full name, film title, length of movie, and a column name "filmlen_groups" that classifies movies based on their length. Filmlen_groups should include 4 categories: 1 hour or less, Between 1-2 hours, Between 2-3 hours, More than 3 hours.

    ```sql
    SELECT 
    	CONCAT(first_name,' ',last_name) AS actor_full_name,
    	film.title,
        film.length,
        (CASE film.length
         	WHEN film.length <=60 THEN '1 hour or less'
         	WHEN film.length <=120 THEN 'Between 1-2 hours'
         	WHEN film.length <=180 THEN 'Between 2-3 hours' 
          	WHEN film.length > 180 THEN 'More than 3 hours'
         	ELSE 'film length N/A' END) AS filmlen_group
        
        FROM actor
        JOIN film_actor
        ON actor.actor_id = film_actor.actor_id
        JOIN film
        ON film_actor.film_id = film.film_id
        GROUP BY 1;
    ```

    

# Insight 1. Family Movie Rentals by Category

Question 1 from Question Set 1 

We want to understand more about the movies that families are watching. The following categories are considered family movies: Animation, Children, Classics, Comedy, Family and Music.

**Create a query that lists each movie, the film category it is classified in, and the number of times it has been rented out.**

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

We want to find out how the two stores compare in their count of rental orders during every month for all the years we have data for. **Write a query that returns the store ID for the store, the year and month and the number of rental orders each store has fulfilled for that month. Your table should include a column for each of the following: year, month, store ID and count of rental orders fulfilled during that month.**

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

We would like to know who were our top 10 paying customers, how many payments they made on a monthly basis during 2007, and what was the amount of the monthly payments. **Can you write a query to capture the customer name, month and year of payment, and total payment amount for each month by these top 10 paying customers?**

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

Finally, for each of these top 10 paying customers, I would like to find out the difference across their monthly payments during 2007. Please go ahead and **write a query to compare the payment amounts in each successive month.** Repeat this for each of these 10 paying customers. Also, it will be tremendously helpful if you can identify the customer name who paid the most difference in terms of payments.

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



