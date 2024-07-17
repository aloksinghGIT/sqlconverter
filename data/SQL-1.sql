SET SERVEROUTPUT ON
 
DECLARE
 
  /* Declaring the collection type */
 
  TYPE t_bulk_collect_test_tab IS TABLE OF test_table%ROWTYPE;
 
  /* Declaring the collection variable */
 
  l_tab t_bulk_collect_test_tab;
 
  CURSOR c_data IS SELECT * FROM test_table;
 
BEGIN
 
  /* Populate the array using BULK COLLECT that retrieves all rows in a single FETCH ,
     getting rid of row by row fetch in a loop */
 
  OPEN c_data;
  FETCH c_data BULK COLLECT INTO l_tab;
  CLOSE c_data;
 
  -- Process contents of collection here.
  DBMS_OUTPUT.put_line(l_tab.count || ' rows');
 
/* Accessing the collection type - Before Modify */
    FOR i IN l_tab.FIRST .. l_tab.LAST 
    LOOP
       EXIT WHEN i = 3;
       dbms_output.put_line('Before Modify- Row- '|| i || ': is '||l_tab(i).name);
       dbms_output.put_line('Before Modify- Row- '|| i || ': is '||l_tab(i).name);
    END LOOP;
 
/* Modifying collection element values */
    l_tab(2).name := 'Change Me';
 
/* Accessing the collection type – After Modify */
    FOR i IN l_tab.FIRST .. l_tab.LAST 
    LOOP
       EXIT WHEN i = 3;
       dbms_output.put_line('After Modify- Row- '|| i || ': is '||l_tab(i).name);
    END LOOP;
 
   dbms_output.put_line('Program executed successfully.');
 
END;