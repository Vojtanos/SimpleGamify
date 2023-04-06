backend
python3 -m venv .gamify-env  
source .gamify-env/bin/activate
pip install -r requirements.txt
python3 app.py

** přes docker **
docker compose up

** Při instalaci nového balíčku na FE **
docker-compose up -d —build
nebo po auktualizaci package.json přímo v dockercontaineru spustit také 
npm i

** backend **
http://localhost:5001/

** mongo-express pro mongodb **
http://localhost:8081/