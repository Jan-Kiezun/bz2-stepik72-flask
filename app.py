from flask import Flask, request, jsonify
from neo4j import GraphDatabase, basic_auth
from neo4j._async.driver import AsyncGraphDatabase
import asyncio

app = Flask(__name__)
driver = AsyncGraphDatabase.driver(
    "bolt://127.0.0.1:7687", auth=basic_auth("neo4j", "test1234")
)


@app.route("/")
async def hello_world():
    async with driver.session() as session:
        data = await session.run("MATCH (n)-[r]->(m) RETURN n,r,m")
        print(data)
        session.close()
        return str(data) + "!" + "\n" + "query"


# @app.route("/employees/<filter_option>/<sort_key>", methods=["GET"])
# async def get_employees(filter_option, sort_key):
#     async with driver.session() as session:
#         [filter_key, filter_value] = filter_option.split("=")
#         query = f'MATCH (n:Employee) WHERE n.{filter_key}="{filter_value}" RETURN n ORDER BY n.{sort_key}'
#         coroutine = await session.run(query)
#         data = await coroutine.data()
#         await session.close()
#         return str(data)


@app.route("/employees", methods=["GET"])
async def get_all_employees():
    async with driver.session() as session:
        filter_option = request.args.get("filter")
        sort_key = request.args.get("sort")
        if filter_option:
            [filter_key, filter_value] = filter_option.split("-")

        whereClause = f'WHERE n.{filter_key}="{filter_value}"' if filter_option else ""
        orderClause = "ORDER BY n." + sort_key if sort_key else ""
        query = f"MATCH (n:Employee) {whereClause} RETURN n {orderClause}"

        coroutine = await session.run(query)
        data = await coroutine.data()
        await session.close()
        return str(data)


@app.route("/employees", methods=["POST"])
async def create_employee():
    data = request.get_json()
    firstname = data["firstname"]
    lastname = data["lastname"]
    age = data["age"]
    salary = data["salary"]
    department = data["department"]
    position = data["position"]
    async with driver.session() as session:
        query = "MERGE (n:Employee {firstname:$firstname,lastname:$lastname,age:$age,salary:$salary,department:$department,position:$position}) MERGE (d:Department {name:$department}) MERGE (n)-[:WORKS_IN]->(d)"
        await session.run(
            query,
            firstname=firstname,
            lastname=lastname,
            age=age,
            salary=salary,
            department=department,
            position=position,
        )
        await session.close()
        return "Employee creation passed"


@app.route("/employees/<id>", methods=["PUT"])
async def update_employee(id):
    data = request.get_json()
    firstname = data.get("firstname", None)
    lastname = data.get("lastname", None)
    age = data.get("age", None)
    salary = data.get("salary", None)
    department = data.get("department", None)
    position = data.get("position", None)
    print(data, id)
    async with driver.session() as session:
        query = f"MATCH (n:Employee) WHERE ID(n) = {id} SET n.firstname = '{firstname}', n.lastname = '{lastname}', n.age = {age}, n.salary = {salary}, n.department = '{department}', n.position = '{position}'"
        await session.run(query)
        await session.close()
        return "Update went through"


@app.route("/employees/<id>", methods=["DELETE"])
async def delete_employee(id):
    async with driver.session() as session:
        query = f"MATCH (n:Employee) WHERE ID(n) = {id} DETACH DELETE n"
        await session.run(query)
        await session.close()
        return "Delete went through"


@app.route("/employees/<id>/subordinates", methods=["GET"])
async def get_subordinates(id):
    async with driver.session() as session:
        query = f"MATCH (manager:Employee)-[:MANAGES]->(:Department)<-[:WORKS_IN]-(subordinate:Employee) WHERE ID(manager) = {id} AND ID(subordinate) <> {id} RETURN subordinate"
        coroutine = await session.run(query)
        data = await coroutine.data()
        await session.close()
        return str(data)


@app.route("/employees/<id>/departmentInfo", methods=["GET"])
async def get_department_info(id):
    department_info = []
    async with driver.session() as session:
        query = f"MATCH (e:Employee)-[:WORKS_IN]->(department:Department) WHERE ID(e) = {id} RETURN department"
        coroutine = await session.run(query)
        data = await coroutine.data()
        department_info.append(data[0])

        query = f"MATCH (e:Employee)-[:WORKS_IN]->(department:Department)<-[:MANAGES]-(manager:Employee) WHERE ID(e) = {id} RETURN manager"
        coroutine = await session.run(query)
        data = await coroutine.data()
        department_info.append(data[0])

        query = f"MATCH (e:Employee)-[:WORKS_IN]->(department:Department)<-[:WORKS_IN]-(subordinate:Employee) WHERE ID(e) = {id} RETURN count(subordinate)+1 as count"
        coroutine = await session.run(query)
        data = await coroutine.data()
        department_info.append(data)

        await session.close()
    return str(department_info)
