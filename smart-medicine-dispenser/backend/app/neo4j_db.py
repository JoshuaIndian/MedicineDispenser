from neo4j import GraphDatabase

from app.config import (
    NEO4J_URI,
    NEO4J_USERNAME,
    NEO4J_PASSWORD,
    NEO4J_DATABASE,
)

driver = None

if all([NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD]):
    driver = GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
    )


def check_neo4j():
    if driver is None:
        raise RuntimeError(
            "Neo4j is not configured in backend/.env"
        )

    driver.verify_connectivity()

    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("RETURN 1 AS value")
        return result.single()["value"]


def close_neo4j():
    if driver is not None:
        driver.close()