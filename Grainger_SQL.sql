-- SQLite

UPDATE inbound_delivery
SET inbound_diff_delivery = (
  SELECT inbound_delivered_date - po_delivery_date 
  FROM purchase_order_header 
  WHERE purchase_order_header.po_id = inbound_delivery.po_id
);