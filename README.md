# Communication-in-Networks-Bot-Application (CINBA)
CINBA is a suite that offers the following resources to research programs wanting to study networks in laboratory experiments.
The application allows researchers to add bots to a video conference to increase the perceived number of participants in a test session. Additionally, individual bots can send text messages via a chat function during the video conference. 
We hope to include voice messaging in the future. Moreover, research programs can manipulate the current messaging feature to induce psychological variables or create different social situations of interest.

# Jitsi installation
CINBA uses jitsi as backend for conference calls. Please refer to jitsi [documentation](https://jitsi.github.io/handbook/docs/devops-guide/) for how to set up a self-hosted instance 


# Deployment
CINBA was deployed to production on University of Gothenburgs 
[openshift](https://www.redhat.com/en/technologies/cloud-computing/openshift)
platform. Secure communication setting like TSL and CORS are configured with openshift routing. Please see 
[openshift docs](https://docs.openshift.com/container-platform/4.1/networking/routes/secured-routes.html) for routing 
setup. 

Other deployment options are of course possible.


## Run with docker

First build the image by running: 
`docker build -t bots:latest .`

Spin it up by running: 
`docker run --name bots -d -p 8000:5000 -e SECRET_KEY=my_very_secret_key --rm bots:latest`

Point your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Environment variables 
Environment variables can be set either by .env or .flaskenv if you run dev or non docker deployment. 

The DOMAIN ENV is used to point out the domain name(s) for the jitsi instance(s) that should be used
 
SECRET_KEY = 'A long random string'
DOMAINS = 'my.first.jtisi.com,my.second.jitsi.com'

### Installation scripts 
`create_user.py` is used to create system users.
Execute `python create_user.py` and fill in username and password when prompted. 

`install_default_bots.py` is used to batch load the system with bots. The script takes a csv-file as input with the following columns
name,year_of_birth,sex 

Execute `python install_default_bots.py bots.csv`
 
### User guide 
TBD



