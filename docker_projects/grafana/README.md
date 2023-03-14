# Grafana Deployment

The mounted folder for grafana data must be accesible for defaults grafana uid and gid, which is 472. 
Change the dir owner applying

    sudo chown -R 472:472 /grafana_data_path