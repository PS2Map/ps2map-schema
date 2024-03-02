CREATE SCHEMA IF NOT EXISTS map_state;

CREATE TABLE IF NOT EXISTS map_state.zone (
    id                INTEGER    PRIMARY KEY,
    world_id          SMALLINT   NOT NULL,
    enabled           BOOLEAN    NOT NULL,
    owner_faction_id  INTEGER,
    last_capture_time TIMESTAMP,

    FOREIGN KEY (world_id)         REFERENCES game.world(id),
    FOREIGN KEY (owner_faction_id) REFERENCES game.faction(id)
);

CREATE TABLE IF NOT EXISTS map_state.region (
    id                INTEGER,
    world_id          SMALLINT   NOT NULL,
    zone_id           INTEGER    NOT NULL,
    enabled           BOOLEAN    NOT NULL,
    owner_faction_id  INTEGER,
    owner_outfit_id   BIGINT,
    last_capture_time TIMESTAMP,

    PRIMARY KEY (id, world_id),
    FOREIGN KEY (world_id)         REFERENCES game.world(id),
    FOREIGN KEY (zone_id)          REFERENCES game.zone(id),
    FOREIGN KEY (owner_faction_id) REFERENCES game.faction(id)
);
