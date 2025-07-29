import { v4 as uuidv4 } from 'uuid';

export default defineEventHandler((event) => {
    console.log('New request: ' + getRequestURL(event) + " " + uuidv4())
    event.context.uuid = uuidv4()
})