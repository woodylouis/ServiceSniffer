DROP TABLE if exists host;
DROP TABLE if exists service;
DROP TABLE if exists host_service;


CREATE TABLE host (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
host_ip VARCHAR NOT NULL,
port INTEGER NOT NULL,
server_url VARCHAR NOT NULL

);
CREATE TABLE service (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
service_type VARCHAR NOT NULL
);

-- CREATE TABLE host_service (
-- host_id               INTEGER NOT NULL,
-- service_id            INTEGER NOT NULL,
--
-- PRIMARY KEY (host_id, service_id),
-- FOREIGN KEY (host_id) REFERENCES host(id),
-- FOREIGN KEY (service_id) REFERENCES service(id)
-- );

-- INSERT INTO service(id, name, service_type) VALUES (null, "odap", "OPENDAP");
-- INSERT INTO service(id, name, service_type) VALUES (null, "dap4", "DAP4" );
-- INSERT INTO service(id, name, service_type) VALUES (null, "http", "HTTPServer" );
-- INSERT INTO service(id, name, service_type) VALUES (null, "wcs" , "WCS");
-- INSERT INTO service(id, name, service_type) VALUES (null, "wms" , "WMS");
-- INSERT INTO service(id, name, service_type) VALUES (null, "ncss", "NetcdfSubset" );
-- INSERT INTO service(id, name, service_type) VALUES (null, "ncml", "NCML" );
-- INSERT INTO service(id, name, service_type) VALUES (null, "uddc", "UDDC" );
-- INSERT INTO service(id, name, service_type) VALUES (null, "iso" , "ISO");