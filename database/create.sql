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
service_type VARCHAR NOT NULL UNIQUE
);

CREATE TABLE host_service (
host_id               INTEGER NOT NULL,
service_id            INTEGER NOT NULL,

PRIMARY KEY (host_id, service_id),
FOREIGN KEY (host_id) REFERENCES host(id),
FOREIGN KEY (service_id) REFERENCES service(id)
);

INSERT INTO service(service_type) VALUES ("OPENDAP");
INSERT INTO service(service_type) VALUES ("DAP4" );
INSERT INTO service(service_type) VALUES ("HTTPServer" );
INSERT INTO service(service_type) VALUES ("WCS");
INSERT INTO service(service_type) VALUES ("WMS");
INSERT INTO service(service_type) VALUES ("NetcdfSubset" );
INSERT INTO service(service_type) VALUES ("NCML" );
