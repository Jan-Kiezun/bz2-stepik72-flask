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
        print(query)

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
        query = "MATCH (n:Employee {firstname:$firstname,lastname:$lastname,age:$age,salary:$salary,department:$department,position:$position}) MERGE (d:Department {name:$department}) MERGE (n)-[:WORKS_IN]->(d)"
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
        return "Employee created successfully"
