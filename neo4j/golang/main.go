package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/gommon/log"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

var driver neo4j.DriverWithContext

func main() {
	ctx := context.Background()
	driver := connect()
	defer driver.Close(ctx)

	e := echo.New()
	e.Logger.SetLevel(log.INFO)

	e.GET("/", func(c echo.Context) error {
		time.Sleep(5 * time.Second)
		return c.JSON(http.StatusOK, "OK")
	})

	e.POST("/person", createPerson)
	e.GET("/person", findAllPerson)
	e.PUT("/person", PutPerson)
	e.PUT("/person/relationship", changeRelationship)
	e.DELETE("/person/relationship", removeRelationship)
	e.DELETE("/person/node", removeNode)
	e.DELETE("/person/node-relationship", removeNodeAndRelationship)

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()
	// Start server
	go func() {
		if err := e.Start(":8080"); err != nil && err != http.ErrServerClosed {
			e.Logger.Fatal("shutting down the server")
		}
	}()
	// Wait for interrupt signal to gracefully shut down the server with a timeout of 10 seconds.
	<-ctx.Done()
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	if err := e.Shutdown(ctx); err != nil {
		e.Logger.Fatal(err)
	}
}

func connect() neo4j.DriverWithContext {
	var err error
	ctx := context.Background()
	// URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
	dbUri := "neo4j://localhost:7687"
	dbUser := "neo4j"
	dbPassword := "neo4jneo4j"
	driver, err = neo4j.NewDriverWithContext(
		dbUri,
		neo4j.BasicAuth(dbUser, dbPassword, ""))
	// defer driver.Close(ctx)

	err = driver.VerifyConnectivity(ctx)
	if err != nil {
		panic(err)
	}
	fmt.Println("Connection established.")
	return driver
}

type CreatePerson struct {
	Name       string `json:"name"`
	FriendName string `json:"friendName"`
}

func createPerson(c echo.Context) error {
	createPerson := new(CreatePerson)
	err := c.Bind(createPerson)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, echo.Map{
			"response": err.Error(),
		})
	}
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    CREATE (a:Person {name: $name})
    CREATE (b:Person {name: $friendName})
    CREATE (a)-[:KNOWS]->(b)
    `,
		map[string]any{
			"name":       "Alice",
			"friendName": "David",
		}, neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())
	return c.JSON(http.StatusOK, echo.Map{
		"nodeCreated":          summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}

func findAllPerson(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    MATCH (p:Person)-[:KNOWS]->(:Person)
    RETURN p.name AS name
    `,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	// Loop through results and do something with them
	for _, record := range result.Records {
		name, _ := record.Get("name") // .Get() 2nd return is whether key is present
		fmt.Println(name)
		// or
		// fmt.Println(record.AsMap())  // get Record as a map
	}

	// Summary information
	fmt.Printf("The query `%v` returned %v records in %+v.\n",
		result.Summary.Query().Text(), len(result.Records),
		result.Summary.ResultAvailableAfter())

	return c.JSON(http.StatusOK, echo.Map{
		"query":                result.Summary.Query().Text(),
		"lenData":              len(result.Records),
		"resultAvailableAfter": result.Summary.ResultAvailableAfter(),
	})
}

func PutPerson(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    MATCH (p:Person {name: 'Alice'})
	SET p.name = 'Alice1'
	RETURN p;
    `,
		map[string]any{},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())

	return c.JSON(http.StatusOK, echo.Map{
		"nodesCreated":         summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}

func changeRelationship(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    	MATCH (a:Person {name: 'David'})-[:KNOWS]->(b:Person {name: 'Alice1'})
		SET a.since = 2020
		RETURN a, b;
    `,
		map[string]any{},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())
	return c.JSON(http.StatusOK, echo.Map{
		"nodesCreated":         summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}

func removeRelationship(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    	MATCH (a:Person {name: 'David'})-[r:KNOWS]->(b:Person {name: 'Alice1'})
		DELETE r;
    `,
		map[string]any{},
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())
	return c.JSON(http.StatusOK, echo.Map{
		"nodesCreated":         summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}

func removeNode(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    	MATCH (p:Person {name: 'David'})
		DELETE p;
    `,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())
	return c.JSON(http.StatusOK, echo.Map{
		"nodesCreated":         summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}

func removeNodeAndRelationship(c echo.Context) error {
	result, err := neo4j.ExecuteQuery(c.Request().Context(), driver, `
    	MATCH (p:Person {name: 'David'})
		DETACH DELETE p;
    `,
		nil,
		neo4j.EagerResultTransformer,
		neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		panic(err)
	}

	summary := result.Summary
	fmt.Printf("Created %v nodes in %+v.\n",
		summary.Counters().NodesCreated(),
		summary.ResultAvailableAfter())
	return c.JSON(http.StatusOK, echo.Map{
		"nodesCreated":         summary.Counters().NodesCreated(),
		"resultAvailableAfter": summary.ResultAvailableAfter(),
	})
}
