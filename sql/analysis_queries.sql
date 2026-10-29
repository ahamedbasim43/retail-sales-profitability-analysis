
-- QUERY 1: Total sales, profit, quantity and order count
SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    SUM(Quantity) AS total_quantity,
    COUNT(DISTINCT "Order ID") AS total_orders
FROM superstore;


-- QUERY 2: Category-wise sales and profit
SELECT
    Category,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM superstore
GROUP BY Category
ORDER BY total_sales DESC;


-- QUERY 3: Region-wise performance
SELECT
    Region,
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM superstore
GROUP BY Region
ORDER BY total_profit DESC;


-- QUERY 4: Monthly sales trend
SELECT
    strftime('%Y-%m', "Order Date") AS sales_month,
    ROUND(SUM(Sales), 2) AS monthly_sales,
    ROUND(SUM(Profit), 2) AS monthly_profit
FROM superstore
GROUP BY strftime('%Y-%m', "Order Date")
ORDER BY sales_month;


-- QUERY 5: Top 10 products by sales
SELECT
    "Product Name",
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM superstore
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10;


-- QUERY 6: Loss-making sub-categories
SELECT
    "Sub-Category",
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM superstore
GROUP BY "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY total_profit ASC;


-- QUERY 7: Discount versus profit
SELECT
    Discount,
    COUNT(*) AS transaction_lines,
    ROUND(AVG(Profit), 2) AS average_profit,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Sales), 2) AS total_sales
FROM superstore
GROUP BY Discount
ORDER BY Discount;


-- QUERY 8: Monthly order count
SELECT
    strftime('%Y-%m', "Order Date") AS sales_month,
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(AVG(Sales), 2) AS average_line_sales
FROM superstore
GROUP BY strftime('%Y-%m', "Order Date")
ORDER BY sales_month;
