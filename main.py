import discord

from os import urandom
from github import Github, GithubIntegration
from src.defines import TOKEN, GUILD, TARGET_CHANNEL, GITHUB_APP_ID, GITHUB_CLIENT_ID
from src.input_proccesors.vote import Vote
from src.input_proccesors.suggestion import Suggestion

github_integration = GithubIntegration(GITHUB_APP_ID, open('angry-villager.2020-10-03.private-key.pem', 'r').read())
installation = github_integration.get_installation('OutlawByteStudios', 'KingdomsDiscordBot')
token = github_integration.create_jwt()


github_client = Github('v1.e9827ef3291f575ac58d4def4ab428afc868806e')
client = discord.Client()

# Suggestions project = 5594461
# Suggestions column = 11079851
# Project Plan project id = 5594457
project_kingdoms_suggestions_repo = github_client.get_repo(
    'OutlawByteStudios/KingdomsDiscordBot')
suggestion_column = github_client.get_project_column(11079851)
suggestion_label = project_kingdoms_suggestions_repo.get_label('suggestion')


vote = Vote(project_kingdoms_suggestions_repo)
suggestion = Suggestion(project_kingdoms_suggestions_repo,
                        suggestion_column, suggestion_label)

print(f'Repo has {project_kingdoms_suggestions_repo.open_issues} open issues')


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.name != TARGET_CHANNEL:
        print('Wrong channel')
        return
    if not check_input(['!vote', '**Suggestion**'], message):
        print('Wrong command')
        return
    await process_input(message)


client.run(TOKEN)


def check_input(list, message) -> bool:
    for start_str in list:
        if message.content.startswith(start_str):
            return True
    return False


async def process_input(message):
    if message.content.startswith('!vote'):
        await vote.process(message)
    elif message.content.startswith('**Suggestion**'):
        await suggestion.process(message)
