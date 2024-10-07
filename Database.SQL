#Create table for material master#
CREATE TABLE 'Material Master' 
( mat_id VARCHAR(20) PRIMARY KEY, mat_name VARCHAR(255) NOT NULL, mat_unit_cost DECIMAL(10, 2) NOT NULL, mat_warranty INT );

#Create table for vendor table#
CREATE TABLE 'Vendors' 
( vendor_id VARCHAR(20) PRIMARY KEY, vendor_name VARCHAR(255) NOT NULL );

#Create table for customer table#
CREATE TABLE 'Customers' 
( customer_id VARCHAR(20) PRIMARY KEY, customer_name VARCHAR(255) NOT NULL );


