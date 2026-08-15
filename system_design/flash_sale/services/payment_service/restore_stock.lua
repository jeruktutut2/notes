-- restore_stock.lua
-- KEYS[1] = flash_sale:{sale_id}:stock
-- KEYS[2] = flash_sale:{sale_id}:purchased
-- KEYS[3] = flash_sale:{sale_id}:status
-- ARGV[1] = user_id

local new_stock = redis.call('INCR', KEYS[1])
redis.call('SREM', KEYS[2], ARGV[1])

local status = redis.call('GET', KEYS[3])
if status == 'SOLD_OUT' and new_stock > 0 then
    redis.call('SET', KEYS[3], 'ACTIVE')
end

return {new_stock, 'RESTORED'}
