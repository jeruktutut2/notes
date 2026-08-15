-- deduct_stock.lua
-- KEYS[1] = flash_sale:{sale_id}:stock
-- KEYS[2] = flash_sale:{sale_id}:purchased
-- KEYS[3] = flash_sale:{sale_id}:status
-- ARGV[1] = user_id

local status = redis.call('GET', KEYS[3])
if status ~= 'ACTIVE' then
    return {-2, 'SALE_NOT_ACTIVE'}
end

local already_purchased = redis.call('SISMEMBER', KEYS[2], ARGV[1])
if already_purchased == 1 then
    return {-3, 'ALREADY_PURCHASED'}
end

local current_stock = tonumber(redis.call('GET', KEYS[1]))
if current_stock == nil or current_stock <= 0 then
    redis.call('SET', KEYS[3], 'SOLD_OUT')
    return {-1, 'SOLD_OUT'}
end

local remaining = redis.call('DECR', KEYS[1])
redis.call('SADD', KEYS[2], ARGV[1])

if remaining <= 0 then
    redis.call('SET', KEYS[3], 'SOLD_OUT')
end

return {remaining, 'SUCCESS'}
