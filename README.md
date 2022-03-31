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

#### Main application window 
The main application window lists all available calls.
 
![Main window](/screenshots/main.png)

Adding new calls is done from the action menu.

![Add call](/screenshots/add_call.png)

![Add call modal](/screenshots/add_chat_modal.png)

By clicking either the "view" button or the calls title will open the calls detail view. 
From the detail views action menu bots can be added. 

#### Call detail view

![Detail action menu](/screenshots/detail_action.png)

The add bot modal takes the following arguments:
* Number of bots to genarate
* Year of birth start/end (Used to filter bots that fall in a range of years)
* Sex
* Generate random participant ids (If checked the application will add some random alphanumeric numbers to the botnames)

![Bot modal](/screenshots/random_bot_modal.PNG)


![Detail view](/screenshots/detail.png)

Start the call by clicking **Open meeting** in the action menu

#### Bot puppeteer view
The bot Bot puppeteer view will open a call for each bot in a frame. 

![Bots window](/screenshots/bots_run.png)

From the action menu there are two quick functions one for toggling the chat windows of jitsi and one for disconnecting 
all the bots with one click which can be used to simulate a breakout room (A function that is not available in jitsi )

![Bots action menu](/screenshots/bots_run_action.png)

#### Participant view 

The conference call as seen by the participant.

![Participant view](/screenshots/participant_view.png)

