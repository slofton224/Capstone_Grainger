#Create table for material master#
CREATE TABLE 'Material Master' 
( mat_id VARCHAR(20) PRIMARY KEY, mat_name VARCHAR(255) NOT NULL, mat_unit_cost DECIMAL(10, 2) NOT NULL, mat_warranty INT );

#Create table for vendors#
CREATE TABLE 'Vendors' 
( vendor_id VARCHAR(20) PRIMARY KEY, vendor_name VARCHAR(255) NOT NULL );

#Create table for customers#
CREATE TABLE 'Customers' 
( customer_id VARCHAR(20) PRIMARY KEY, customer_name VARCHAR(255) NOT NULL );

#Create table for purchase info records#
CREATE TABLE 'Purchase Info Records' 
( pir_id VARCHAR(20) PRIMARY KEY, vendor_id VARCHAR(20) NOT NULL, mat_id VARCHAR(255) NOT NULL );

#Create table for purchase orders#
CREATE TABLE 'Purchase Orders' 
( po_id VARCHAR(20) PRIMARY KEY, vendor_id VARCHAR(20) NOT NULL, po_net_cost DECIMAL (10, 2) NOT NULL, po_date DATE, po_delivery_date DATE );

#Create table for purchase order items#
CREATE TABLE 'Purchase Order Items' 
( po_id VARCHAR(20) PRIMARY KEY, mat_id VARCHAR(20) NOT NULL, po_qty INT, po_unit_cost DECIMAL (10, 2) NOT NULL );

#Create table for inbound deliveries#
CREATE TABLE 'Inbound Delivery' 
( inbound_id VARCHAR(20) PRIMARY KEY, po_id VARCHAR(20) NOT NULL, mat_id VARCHAR(255) NOT NULL, inbound_received_qty INT, inbound_delivered_date DATE, inbound_failed_qty INT, inbound_diff_qty INT, inbound_diff_delivery INT );

#Create table for sales orders#
CREATE TABLE 'Sales Orders' 
( so_id VARCHAR(20) PRIMARY KEY, customer_id VARCHAR(20) NOT NULL, so_created_on DATE, so_order_type VARCHAR(20), so_net_value DEECIMAL (10, 2) NOT NULL );

#Create table for sales order items#
CREATE TABLE 'Sales Order Items' 
( so_id VARCHAR(20) PRIMARY KEY, mat_id VARCHAR(20) NOT NULL, so_qty INT, so_sell_price DECIMAL (10, 2) NOT NULL, so_returned_against VARCHAR(20) );

#Create table for customer reviews#
CREATE TABLE 'Customer Reviews' 
( review_id VARCHAR(20) PRIMARY KEY, so_id VARCHAR(20) NOT NULL, mat_id VARCHAR(20) NOT NULL, customer_rating INT, so_sell_price DECIMAL (10, 2) NOT NULL, so_returned_against VARCHAR(20) );

#Calculate Differences in Delivery Dates and Quantity in Inbound Delivery

SELECT 
    ID.inbound_id,
    ID.po_id,
    DATEDIFF(ID.inbound_delivered_date, PO.po_delivery_date) AS DeliveryDateDifference,
    (ID.inbound_received_qty - ID.inbound_diff_qty) AS QuantityDifference
FROM 
    `Inbound Delivery` AS ID
JOIN 
    `Purchase Orders` AS PO
ON 
    ID.po_id = PO.po_id;



    # Calculate Return Pre/Post Warranty
SELECT 
    SOI.so_id,
    SOI.mat_id,
    SOI.so_returned_against,
    MM.mat_warranty,
    CASE 
        WHEN DATEDIFF(SOI.so_returned_against, SO.so_created_on) <= MM.mat_warranty 
        THEN 'Pre-Warranty Return'
        ELSE 'Post-Warranty Return'
    END AS ReturnStatus
FROM 
    `Sales Order Items` AS SOI
JOIN 
    `Sales Orders` AS SO
ON 
    SOI.so_id = SO.so_id
JOIN 
    `Material Master` AS MM
ON 
    SOI.mat_id = MM.mat_id
WHERE 
    SOI.so_returned_against IS NOT NULL; 