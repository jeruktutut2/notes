# NEO4J

## docker 
    docker pull neo4j:5.26.10-community-ubi9

    docker run \
    --name=neo4j \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=neo4j/neo4jneo4j \
    -d neo4j:5.26.10-community-ubi9

    docker run \
    --name=neo4j \
    --restart always \
    --publish=7474:7474 --publish=7687:7687 \
    --env NEO4J_AUTH=none \
    -d neo4j:5.26.10-community-ubi9

    http://localhost:7474/ browser

    docker exec -it neo4j bash
    cypher-shell -u neo4j -p neo4jneo4j
    SHOW DATABASES;
    CALL db.labels(); untuk melihat semua label
    MATCH (p:Person) RETURN p; untuk melihat semua isi tabel
    CREATE DATABASE test1;
    USE test1;
    :exit

    install plugin gds
    docker compose up -d
    docker compose -f docker-compose.yaml up -d
    docker compose down
    docker compose down -v
    docker compose stop
    Opsi -v = delete volumes yang terdefinisi di docker-compose.yml.
    CALL gds.version();
    docker logs neo4j

    // 50 Nodes: Kota
    CREATE (:City {name: 'Jakarta'}), (:City {name: 'Surabaya'}), (:City {name: 'Bandung'}),
       (:City {name: 'Medan'}), (:City {name: 'Makassar'}), (:City {name: 'Denpasar'}),
       (:City {name: 'Palembang'}), (:City {name: 'Semarang'}), (:City {name: 'Yogyakarta'}),
       (:City {name: 'Balikpapan'}), (:City {name: 'Padang'}), (:City {name: 'Pekanbaru'}),
       (:City {name: 'Manado'}), (:City {name: 'Batam'}), (:City {name: 'Malang'}),
       (:City {name: 'Lampung'}), (:City {name: 'Pontianak'}), (:City {name: 'Samarinda'}),
       (:City {name: 'Palu'}), (:City {name: 'Kupang'}), (:City {name: 'Banjarmasin'}),
       (:City {name: 'Tanjung Pinang'}), (:City {name: 'Jambi'}), (:City {name: 'Pangkal Pinang'}),
       (:City {name: 'Tarakan'}), (:City {name: 'Ternate'}), (:City {name: 'Kendari'}),
       (:City {name: 'Ambon'}), (:City {name: 'Merauke'}), (:City {name: 'Jayapura'}),
       (:City {name: 'Banda Aceh'}), (:City {name: 'Lombok'}), (:City {name: 'Kuala Lumpur'}),
       (:City {name: 'Singapore'}), (:City {name: 'Bangkok'}), (:City {name: 'Ho Chi Minh City'}),
       (:City {name: 'Manila'}), (:City {name: 'Hong Kong'}), (:City {name: 'Tokyo'}),
       (:City {name: 'Seoul'}), (:City {name: 'Beijing'}), (:City {name: 'Shanghai'}),
       (:City {name: 'Dubai'}), (:City {name: 'Sydney'}), (:City {name: 'Perth'}),
       (:City {name: 'London'}), (:City {name: 'Paris'}), (:City {name: 'Berlin'}),
       (:City {name: 'New York'}), (:City {name: 'Los Angeles'});

    // 50 Relationships: Rute Penerbangan
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Surabaya'}) CREATE (a)-[:FLIGHT {distance: 690}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Denpasar'}) CREATE (a)-[:FLIGHT {distance: 985}]->(b);
    MATCH (a:City {name: 'Surabaya'}), (b:City {name: 'Makassar'}) CREATE (a)-[:FLIGHT {distance: 835}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Singapore'}) CREATE (a)-[:FLIGHT {distance: 884}]->(b);
    MATCH (a:City {name: 'Denpasar'}), (b:City {name: 'Tokyo'}) CREATE (a)-[:FLIGHT {distance: 5543}]->(b);
    MATCH (a:City {name: 'Singapore'}), (b:City {name: 'Tokyo'}) CREATE (a)-[:FLIGHT {distance: 5323}]->(b);
    MATCH (a:City {name: 'Tokyo'}), (b:City {name: 'New York'}) CREATE (a)-[:FLIGHT {distance: 10850}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Bangkok'}) CREATE (a)-[:FLIGHT {distance: 2337}]->(b);
    MATCH (a:City {name: 'Bangkok'}), (b:City {name: 'Dubai'}) CREATE (a)-[:FLIGHT {distance: 4880}]->(b);
    MATCH (a:City {name: 'Dubai'}), (b:City {name: 'London'}) CREATE (a)-[:FLIGHT {distance: 5493}]->(b);
    MATCH (a:City {name: 'London'}), (b:City {name: 'New York'}) CREATE (a)-[:FLIGHT {distance: 5570}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Kuala Lumpur'}) CREATE (a)-[:FLIGHT {distance: 1125}]->(b);
    MATCH (a:City {name: 'Kuala Lumpur'}), (b:City {name: 'Hong Kong'}) CREATE (a)-[:FLIGHT {distance: 2525}]->(b);
    MATCH (a:City {name: 'Hong Kong'}), (b:City {name: 'Tokyo'}) CREATE (a)-[:FLIGHT {distance: 2977}]->(b);
    MATCH (a:City {name: 'Surabaya'}), (b:City {name: 'Batam'}) CREATE (a)-[:FLIGHT {distance: 840}]->(b);
    MATCH (a:City {name: 'Batam'}), (b:City {name: 'Singapore'}) CREATE (a)-[:FLIGHT {distance: 20}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Beijing'}) CREATE (a)-[:FLIGHT {distance: 4385}]->(b);
    MATCH (a:City {name: 'Beijing'}), (b:City {name: 'Shanghai'}) CREATE (a)-[:FLIGHT {distance: 1067}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Sydney'}) CREATE (a)-[:FLIGHT {distance: 4480}]->(b);
    MATCH (a:City {name: 'Sydney'}), (b:City {name: 'New York'}) CREATE (a)-[:FLIGHT {distance: 16000}]->(b);
    MATCH (a:City {name: 'Denpasar'}), (b:City {name: 'Sydney'}) CREATE (a)-[:FLIGHT {distance: 4600}]->(b);
    MATCH (a:City {name: 'Makassar'}), (b:City {name: 'Jayapura'}) CREATE (a)-[:FLIGHT {distance: 1700}]->(b);
    MATCH (a:City {name: 'Jayapura'}), (b:City {name: 'Sydney'}) CREATE (a)-[:FLIGHT {distance: 2800}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Padang'}) CREATE (a)-[:FLIGHT {distance: 933}]->(b);
    MATCH (a:City {name: 'Padang'}), (b:City {name: 'Banda Aceh'}) CREATE (a)-[:FLIGHT {distance: 690}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Medan'}) CREATE (a)-[:FLIGHT {distance: 1400}]->(b);
    MATCH (a:City {name: 'Medan'}), (b:City {name: 'Kuala Lumpur'}) CREATE (a)-[:FLIGHT {distance: 350}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Palembang'}) CREATE (a)-[:FLIGHT {distance: 450}]->(b);
    MATCH (a:City {name: 'Palembang'}), (b:City {name: 'Pangkal Pinang'}) CREATE (a)-[:FLIGHT {distance: 200}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Yogyakarta'}) CREATE (a)-[:FLIGHT {distance: 425}]->(b);
    MATCH (a:City {name: 'Yogyakarta'}), (b:City {name: 'Balikpapan'}) CREATE (a)-[:FLIGHT {distance: 1200}]->(b);
    MATCH (a:City {name: 'Balikpapan'}), (b:City {name: 'Samarinda'}) CREATE (a)-[:FLIGHT {distance: 50}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Pontianak'}) CREATE (a)-[:FLIGHT {distance: 720}]->(b);
    MATCH (a:City {name: 'Pontianak'}), (b:City {name: 'Batam'}) CREATE (a)-[:FLIGHT {distance: 575}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Lampung'}) CREATE (a)-[:FLIGHT {distance: 190}]->(b);
    MATCH (a:City {name: 'Lampung'}), (b:City {name: 'Denpasar'}) CREATE (a)-[:FLIGHT {distance: 1000}]->(b);
    MATCH (a:City {name: 'Bandung'}), (b:City {name: 'Medan'}) CREATE (a)-[:FLIGHT {distance: 1500}]->(b);
    MATCH (a:City {name: 'Bandung'}), (b:City {name: 'Denpasar'}) CREATE (a)-[:FLIGHT {distance: 800}]->(b);
    MATCH (a:City {name: 'Yogyakarta'}), (b:City {name: 'Lombok'}) CREATE (a)-[:FLIGHT {distance: 600}]->(b);
    MATCH (a:City {name: 'Lombok'}), (b:City {name: 'Perth'}) CREATE (a)-[:FLIGHT {distance: 2700}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Semarang'}) CREATE (a)-[:FLIGHT {distance: 360}]->(b);
    MATCH (a:City {name: 'Semarang'}), (b:City {name: 'Malang'}) CREATE (a)-[:FLIGHT {distance: 250}]->(b);
    MATCH (a:City {name: 'Malang'}), (b:City {name: 'Manado'}) CREATE (a)-[:FLIGHT {distance: 1750}]->(b);
    MATCH (a:City {name: 'Manado'}), (b:City {name: 'Tokyo'}) CREATE (a)-[:FLIGHT {distance: 3800}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'Manila'}) CREATE (a)-[:FLIGHT {distance: 2800}]->(b);
    MATCH (a:City {name: 'Manila'}), (b:City {name: 'Seoul'}) CREATE (a)-[:FLIGHT {distance: 2500}]->(b);
    MATCH (a:City {name: 'Seoul'}), (b:City {name: 'Tokyo'}) CREATE (a)-[:FLIGHT {distance: 1200}]->(b);
    MATCH (a:City {name: 'Surabaya'}), (b:City {name: 'Kupang'}) CREATE (a)-[:FLIGHT {distance: 1000}]->(b);
    MATCH (a:City {name: 'Kupang'}), (b:City {name: 'Perth'}) CREATE (a)-[:FLIGHT {distance: 1700}]->(b);
    MATCH (a:City {name: 'Jakarta'}), (b:City {name: 'New York'}) CREATE (a)-[:FLIGHT {distance: 15000}]->(b);

    MATCH (start:City {name: 'Jakarta'}), (end:City {name: 'Tokyo'})
    CALL gds.graph.project('flight-graph', 'City', 'FLIGHT', {relationshipProperties: 'distance'})
    YIELD graphName, nodeCount, relationshipCount
    CALL gds.shortestPath.dijkstra.stream('flight-graph', {
        sourceNode: start,
        targetNode: end,
        relationshipWeightProperty: 'distance'
    })
    YIELD index, sourceNode, targetNode, totalCost, path
    RETURN
        totalCost AS total_distance,
        [n IN nodes(path) | n.name] AS route
    ORDER BY total_distance ASC
    LIMIT 1;

    edit relationship
    MATCH (a:Person {name: 'Jonathan'})-[:KNOWS]->(b:Person {name: 'Jane'})
    SET a.since = 2020
    RETURN a, b;