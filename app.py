from flask import Flask, request, jsonify
from neo4j import GraphDatabase, basic_auth
from neo4j._async.driver import AsyncGraphDatabase

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


@app.route("/employees/<filter_option>/<sort_key>", methods=["GET"])
async def get_employees(filter_option, sort_key):
    async with driver.session() as session:
        [filter_key, filter_value] = filter_option.split("=")
        query = f'MATCH (n:Employee) WHERE n.{filter_key}="{filter_value}" RETURN n ORDER BY n.{sort_key}'
        coroutine = await session.run(query)
        data = await coroutine.data()
        await session.close()
        return str(data)


@app.route("/employees", methods=["GET"])
async def get_all_employees():
    async with driver.session() as session:
        coroutine = await session.run("MATCH (n:Employee) RETURN n")
        data = await coroutine.data()
        await session.close()
        return str(data)


@app.route("/employees", methods=["POST"])
async def create_employee():
    data = request.get_json()
    async with driver.session() as session:
        # query = f"CREATE (n:Employee) SET n={data}"
        query = f"MATCH (n:Employee) RETURN n"
        coroutine = await session.run(query)
        # data = await coroutine.data()
        print(data["data"])
        await session.close()
        return "Employee created successfully"
