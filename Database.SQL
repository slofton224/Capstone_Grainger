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

#####
#Create derived columns#
ALTER TABLE inbound_delivery
ADD COLUMN inbound_diff_qty INTEGER;

ALTER TABLE inbound_delivery
ADD COLUMN inbound_diff_delivery INTEGER;

ALTER TABLE sales_order_item
ADD COLUMN so_warrranty_calculation INTEGER;

ALTER TABLE sales_order_item
ADD COLUMN so_pre_post_warranty TEXT;


#so_diff_qty# -- Difference in PO quantity and received quanity
UPDATE inbound_delivery
SET inbound_diff = inbound_received_qty - pi.po_qty
FROM purchase_order_item pi
WHERE inbound_delivery.po_id = pi.po_id and inbound_delivery.mat_id = pi.mat_id;

#so_diff_delivery# -- Date difference in PO delivery date and actual delivery date
UPDATE inbound_delivery
SET inbound_diff_delivery = (
  SELECT julianday(inbound_delivered_date) - julianday(po_delivery_date) 
  FROM purchase_order_header
  WHERE purchase_order_header.po_id = inbound_delivery.po_id
);

#so_warrranty_calculation# -- Date difference between sales order and return order
UPDATE sales_order_item
SET so_warranty_calculation = (
    SELECT 
        julianday(header_original.so_created_on) - julianday(header_returned.so_created_on)
    FROM 
        sales_order_header AS header_original
    JOIN sales_order_header AS header_returned
        ON sales_order_item.so_returned_against = header_returned.so_id
    WHERE 
        sales_order_item.so_id = header_original.so_id
)
WHERE so_returned_against IS NOT NULL;

#so_pre_post_warranty# -- Determine if return order falls into pre- or post-warranty
UPDATE sales_order_item
SET so_pre_post_warranty = (
    CASE 
        WHEN so_warranty_calculation <= (
            SELECT mat_warranty 
            FROM material_master 
            WHERE material_master.mat_id = sales_order_item.mat_id
        ) THEN 'Pre-warranty'
        ELSE 'Post-warranty'
    END
)
WHERE so_warranty_calculation IS NOT NULL
AND EXISTS (
    SELECT 1 
    FROM material_master 
    WHERE material_master.mat_id = sales_order_item.mat_id
);
