CREATE SCHEMA IF NOT EXISTS game;

CREATE TABLE IF NOT EXISTS game.faction (
    id   SMALLINT    PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    tag  VARCHAR(4)  NOT NULL
);

CREATE TABLE IF NOT EXISTS game.world (
    id       SMALLINT     PRIMARY KEY,
    name     VARCHAR(32)  NOT NULL,
    region   VARCHAR(32),
    platform VARCHAR(16)  NOT NULL
);

CREATE TABLE IF NOT EXISTS game.zone (
    id          INTEGER        PRIMARY KEY,
    name        VARCHAR(32)    NOT NULL,
    description VARCHAR(1024),
    code        VARCHAR(32)    NOT NULL,
    geometry_id INTEGER        NOT NULL,
    hex_size    FLOAT          NOT NULL,
    map_size    INTEGER        NOT NULL,
    dynamic     BOOLEAN        NOT NULL
);

CREATE TABLE IF NOT EXISTS game.outfit_resource (
    id          INTEGER       PRIMARY KEY,
    name        VARCHAR(32),
    description VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS game.facility_type (
    id          INTEGER       PRIMARY KEY,
    name        VARCHAR(32)   NOT NULL,
    description VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS game.facility (
    id                      INTEGER PRIMARY KEY,
    name                    VARCHAR(32) NOT NULL,
    type_id                 INTEGER NOT NULL,
    zone_id                 INTEGER NOT NULL,
    resource_id             INTEGER,
    resource_capture_amount FLOAT,
    resource_tick_amount    FLOAT,

    FOREIGN KEY (type_id)     REFERENCES game.facility_type(id),
    FOREIGN KEY (zone_id)     REFERENCES game.zone(id),
    FOREIGN KEY (resource_id) REFERENCES game.outfit_resource(id)
);

CREATE TABLE IF NOT EXISTS game.map_region (
    id          INTEGER      PRIMARY KEY,
    name        VARCHAR(32),
    facility_id INTEGER,
    zone_id     INTEGER      NOT NULL,
    map_pos_x   REAL         NOT NULL,
    map_pos_y   REAL         NOT NULL,

    FOREIGN KEY (facility_id) REFERENCES game.facility(id),
    FOREIGN KEY (zone_id)     REFERENCES game.zone(id)
);

CREATE TABLE IF NOT EXISTS game.lattice_link (
    zone_id       INTEGER NOT NULL,
    facility_a_id INTEGER NOT NULL,
    facility_b_id INTEGER NOT NULL,

    PRIMARY KEY (facility_a_id, facility_b_id),
    FOREIGN KEY (zone_id)       REFERENCES game.zone(id),
    FOREIGN KEY (facility_a_id) REFERENCES game.facility(id),
    FOREIGN KEY (facility_b_id) REFERENCES game.facility(id)
);
