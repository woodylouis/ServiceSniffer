DROP TABLE if exists hosts;
DROP TABLE if exists services;
DROP TABLE if exists host_services;

CREATE TABLE hosts (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
host_ip VARCHAR NOT NULL,
port INTEGER NOT NULL,
server_url VARCHAR NOT NULL
);

CREATE TABLE services (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
service_type VARCHAR NOT NULL UNIQUE
);

CREATE TABLE host_services (
host_id               INTEGER NOT NULL,
service_id            INTEGER NOT NULL,

PRIMARY KEY (host_id, service_id),
FOREIGN KEY (host_id) REFERENCES hosts(id),
FOREIGN KEY (service_id) REFERENCES services(id)
);

-- INSERT INTO service(service_type) VALUES ("OPENDAP");
-- INSERT INTO service(service_type) VALUES ("DAP4" );
-- INSERT INTO service(service_type) VALUES ("HTTPServer" );
-- INSERT INTO service(service_type) VALUES ("WCS");
-- INSERT INTO service(service_type) VALUES ("WMS");
-- INSERT INTO service(service_type) VALUES ("NetcdfSubset" );
-- INSERT INTO service(service_type) VALUES ("NCML" );
