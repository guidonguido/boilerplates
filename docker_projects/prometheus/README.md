# Prometheus Deployment

## Prometheus
The mounted folder for promehteus db data must be accesible for defaults prometheus uid and gid, which is 65534. 
Change the dir owner applying
  
    sudo chown -R 65534:65534 /prometheus_data_path

  

Read more here: https://github.com/prometheus/prometheus/issues/5976

  
  

## cAdvisor

Latest tag is not updated, check latest release https://github.com/google/cadvisor/releases

Be aware of the fact that if you install docker w/ snap (on ubuntu), */var/lib/docker* does not exists because docker is set up differently.
To find the actual folder you need, run `docker info | grep "Docker Root Dir:"` (mine was /var/snap/docker/common/var-lib-docker).

 
The cAdvisor container is subject to the following issue: https://github.com/google/cadvisor/issues/3241