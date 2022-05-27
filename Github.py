from bs4 import BeautifulSoup as bs
import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import sys
import time

cookies = {
    ....
}

headers = {
    ....
}

class Dataclass:
    def __init__(self):
        self.name = None
        self.pseudo = None
        self.picture_profile = None
        self.followers = None
        self.following = None
        self.contributions = None
        self.organizations = None

    def scrape(url, username):

        response = requests.get(url=url, cookies=cookies, headers=headers)

        if response.status_code != 200:
            print(f'response code = {response.status_code}')
            sys.exit(84)
        soup = bs(response.text, 'lxml')

        tmp = soup.find('span', {'itemprop' : 'name'}).text
        Dataclass.name = tmp.strip()
        # Name
        tmp = soup.find('span', {'itemprop' : 'additionalName'}).text
        Dataclass.pseudo = tmp.strip()
        # Pseudo
        tmp = soup.find('img', {'class':'avatar avatar-user width-full border color-bg-default'}).get('src')
        Dataclass.picture_profile = tmp
        # Link of the image
        tmp = soup.find('a', {'href':f'https://github.com/{username}?tab=followers'}).text
        Dataclass.followers = " ".join(tmp.split())
        # Nb of followers
        tmp = soup.find('a', {'href':f'https://github.com/{username}?tab=following'}).text
        Dataclass.following = " ".join(tmp.split())
        # Nb of following
        tmp = soup.find('h2', {'class': 'f4 text-normal mb-2'}).text
        Dataclass.contributions = " ".join(tmp.split())
        # Nb of contributions
        tmp = soup.find_all('a', {'class': 'avatar-group-item'})
        orgs = str()
        for org in tmp:
            orgs += '- ' + org['aria-label'] + '\n'
        Dataclass.organizations = orgs
        # Organizations

    def Webhook(url):
        webhook = DiscordWebhook(url='...')
        first_text = f'The profile {Dataclass.name} has:\n\t- {Dataclass.followers},\n\t- {Dataclass.following},\n\t- {Dataclass.contributions},\n\t- She/He is a member of :\n{Dataclass.organizations}\n'
        embed = DiscordEmbed(title='Webhook Hub Project', description='', color=' 8b58de')
        embed.set_author(name=Dataclass.name, url=url, icon_url=Dataclass.picture_profile)
        embed.set_image(url=Dataclass.picture_profile)
        embed.set_thumbnail(url=Dataclass.picture_profile)
        embed.set_timestamp()
        embed.add_embed_field(name='Information about the user', value=first_text)
        webhook.add_embed(embed)
        webhook.execute()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(EnvironmentError("Run the program with one argument"))
        sys.exit(84)
    Dataclass()
    url = 'https://github.com/' + sys.argv[1]

    Dataclass.scrape(url, sys.argv[1])
    Dataclass.Webhook(url)

    prev_name = Dataclass.name
    prev_pseudo = Dataclass.pseudo
    prev_picture_profile = Dataclass.picture_profile
    prev_followers = Dataclass.followers
    prev_following = Dataclass.following
    prev_contributions = Dataclass.contributions
    prev_organizations = Dataclass.organizations

    while True:
        time.sleep(60)
        Dataclass.scrape(url, sys.argv[1])
        if Dataclass.name != prev_name or Dataclass.pseudo != prev_pseudo or Dataclass.pseudo != prev_pseudo or Dataclass.picture_profile != prev_picture_profile or Dataclass.followers != prev_followers or Dataclass.following != prev_following or Dataclass.contributions != prev_contributions or Dataclass.organizations != prev_organizations:
            prev_name = Dataclass.name
            prev_pseudo = Dataclass.pseudo
            prev_picture_profile = Dataclass.picture_profile
            prev_followers = Dataclass.followers
            prev_following = Dataclass.following
            prev_contributions = Dataclass.contributions
            prev_organizations = Dataclass.organizations
            Dataclass.Webhook(url)