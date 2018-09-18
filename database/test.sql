-- select nc_files.id, host_ip, service_type, server_url, nc_name, url_path as NC_File_Path
-- from nc_files
-- INNER JOIN hosts ON hosts.id = nc_files.host_id
-- INNER JOIN services ON services.id = nc_files.service_id;


select hosts.id, hosts.host_ip, services.service_type
from host_services
inner join hosts on hosts.id = host_services.host_id
inner join services on services.id = host_services.service_id;

