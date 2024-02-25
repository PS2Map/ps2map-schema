CREATE SCHEMA IF NOT EXISTS api;

CREATE OR REPLACE VIEW api.server AS
    SELECT id, name, region, platform FROM game.world;

CREATE OR REPLACE VIEW api.continent AS
    SELECT id, name, code, description, map_size FROM game.zone WHERE dynamic = FALSE;

CREATE OR REPLACE VIEW api.base AS
    SELECT r.id, r.zone_id AS continent_id, r.name, r.map_pos_x, r.map_pos_y, ft.name AS type_name, ft.id AS type_code, f.resource_capture_amount, f.resource_tick_amount AS resource_control_amount, res.name AS resource_name, res.id AS resource_code
    FROM game.map_region r
    JOIN game.facility f ON r.facility_id = f.id
    JOIN game.facility_type ft ON f.type_id = ft.id
    FULL OUTER JOIN game.outfit_resource res ON f.resource_id = res.id;

CREATE OR REPLACE VIEW api.lattice AS
    SELECT ra.id AS base_a_id, rb.id AS base_b_id, l.zone_id AS continent_id, ra.map_pos_x AS map_pos_a_x, ra.map_pos_y AS map_pos_a_y, rb.map_pos_x AS map_pos_b_x, rb.map_pos_y AS map_pos_b_y
    FROM game.lattice_link l
    JOIN game.facility fta ON l.facility_a_id = fta.id
    JOIN game.facility ftb ON l.facility_b_id = ftb.id
    JOIN game.map_region ra ON fta.id = ra.facility_id
    JOIN game.map_region rb ON ftb.id = rb.facility_id;
