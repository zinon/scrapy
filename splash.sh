#run docker
sudo systemctl start docker
sudo systemctl enable docker
docker --version

#pull image
sudo docker pull scrapinghub/splash

#run image
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash

#run image / request splash to wait for rendering (suitable for many calls)
#see https://www.baierl.com/new-inventory/
sudo docker run -p 5023:5023 -p 8050:8050 -p 8051:8051 scrapinghub/splash --max-timeout 36

#rendering service for splash
http://0.0.0.0:8050
