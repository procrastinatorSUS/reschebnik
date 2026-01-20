# project name
reshebnik

## description
!TELEGRAM BOT IN WORKING!

a telegram bot for preparing my students for the Unified State Exam in computer science


## quick start

### project setup
```bash 
# clone repo
git clone https://github.com/procrastinatorSUS/reschebnik.git

# in project:
python -m venv .venv

# activate
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# requirements
pip install -r requirements.txt

# .env from example
cp .env.example .env
# edit .env with your settings

```

### server connection

```bash
#to connect to your server, you need to share with ssh key pair

#create own ssh key
ssh-keygen -t ed25519

ssh-copy-id -i ~\.ssh\id_ed25519.pub username@server_ip
```

