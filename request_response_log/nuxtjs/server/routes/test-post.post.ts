// import logMiddleware from "../middleware/test-post-log"

export default defineEventHandler(async (event) => {
    // logMiddleware(event)
    // https://nuxt.com/docs/guide/directory-structure/middleware
    // becouse couldn't find how to create middleware for spesific route, you can do:
    // 1. create global (server/middleware) middleware, add if for spesific route to it
    // 2. or create in page middleware
    // 3. dont forget to seperate middleware responses between html and json
    console.log("controller post")
    return {
        "test": "post",
    }
})