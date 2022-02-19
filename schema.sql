CREATE TABLE IF NOT EXISTS chatbot (
    channel_id BIGINT PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS levels_config (
    guild_id BIGINT PRIMARY KEY,
    channel_id BIGINT,
    ping TEXT
);
CREATE TABLE IF NOT EXISTS prefix (
    user_id BIGINT PRIMARY KEY,
    prefixes TEXT
);
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    guild_id BIGINT,
    xp INT, 
    level INT,
    name TEXT
);