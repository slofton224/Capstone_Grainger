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
( pir_id VARCHAR(20) PRIMARY KEY, vendor_id VARCHAR(255) NOT NULL, mat_id VARCHAR(255) NOT NULL);

#Create table for purchase orders#
CREATE TABLE 'Purchase Orders' 
( po_id VARCHAR(20) PRIMARY KEY, vendor_id VARCHAR(255) NOT NULL, po_net_cost DECIMAL (10, 2) NOT NULL, po_date DATE, po_delivery_date DATE);
