-- SQLite

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

