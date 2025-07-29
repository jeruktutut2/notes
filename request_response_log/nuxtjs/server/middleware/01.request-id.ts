import { v4 as uuidv4 } from 'uuid';

export default defineEventHandler((event) => {
    event.context.uuid = uuidv4()
})