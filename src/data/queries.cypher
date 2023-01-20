CREATE (e1:Employee { firstname: 'John', lastname: 'Doe', age: 30, salary: 10000, department: 'IT', position: 'Manager' }),
(e2:Employee { firstname: 'Jane', lastname: 'Doe', age: 25, salary: 8000, department: 'IT', position: 'Developer' }),
(e3:Employee { firstname: 'John', lastname: 'Smith', age: 35, salary: 15000, department: 'IT', position: 'Developer' }),
(e4:Employee { firstname: 'Jane', lastname: 'Smith', age: 40, salary: 20000, department: 'IT', position: 'Developer' }),
(e5:Employee { firstname: 'Bob', lastname: 'Doe', age: 30, salary: 10000, department: 'HR', position: 'Manager' }),
(e6:Employee { firstname: 'Bailey', lastname: 'Doe', age: 25, salary: 8000, department: 'HR', position: 'Developer' }),
(e7:Employee { firstname: 'Bob', lastname: 'Smith', age: 35, salary: 15000, department: 'HR', position: 'Developer' }),
(e8:Employee { firstname: 'Bailey', lastname: 'Smith', age: 40, salary: 20000, department: 'HR', position: 'Developer' }),
(e9:Employee { firstname: 'Kyle', lastname: 'Doe', age: 30, salary: 10000, department: 'Marketing', position: 'Manager' }),
(e10:Employee { firstname: 'Kristie', lastname: 'Doe', age: 25, salary: 8000, department: 'Marketing', position: 'Developer' }),
(e11:Employee { firstname: 'Kyle', lastname: 'Smith', age: 35, salary: 15000, department: 'Marketing', position: 'Developer' }),
(e12:Employee { firstname: 'Kristie', lastname: 'Smith', age: 40, salary: 20000, department: 'Marketing', position: 'Developer' }),
(e13:Employee { firstname: 'Mike', lastname: 'Doe', age: 30, salary: 10000, department: 'Sales', position: 'Manager' }),
(e14:Employee { firstname: 'Mary', lastname: 'Doe', age: 25, salary: 8000, department: 'Sales', position: 'Developer' }),
(e15:Employee { firstname: 'Mike', lastname: 'Smith', age: 35, salary: 15000, department: 'Sales', position: 'Developer' });

CREATE (d1:Department { name: 'IT', location: 'London' }),
(d2:Department { name: 'HR', location: 'Edinburgh' }),
(d3:Department { name: 'Marketing', location: 'London' }),
(d4:Department { name: 'Sales', location: 'Birmingham' });

MATCH (e1:Employee), (d1:Department)
WHERE e1.department = d1.name
CREATE (e1)-[r:WORKS_IN]->(d1);

MATCH (e1:Employee { firstname:"John", lastname:"Doe" }), (d1:Department {name:"IT"})
CREATE (e1)-[r:MANAGES]->(d1);

MATCH (e1:Employee { firstname:"Bob", lastname:"Doe" }), (d1:Department {name:"HR"})
CREATE (e1)-[r:MANAGES]->(d1);

MATCH (e1:Employee { firstname:"Kyle", lastname:"Doe" }), (d1:Department {name:"Marketing"})
CREATE (e1)-[r:MANAGES]->(d1);

MATCH (e1:Employee { firstname:"Mike", lastname:"Doe" }), (d1:Department {name:"Sales"})
CREATE (e1)-[r:MANAGES]->(d1)
