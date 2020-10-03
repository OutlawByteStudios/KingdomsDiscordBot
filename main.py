import discord

from os import urandom
from github import Github
from src.defines import TOKEN, GUILD, TARGET_CHANNEL, GITHUB_TOKEN
from src.input_proccesors.vote import Vote
from src.input_proccesors.suggestion import Suggestion

github_client = Github(GITHUB_TOKEN)
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
        return
    if not check_input(['!vote', '**Suggestion**'], message):
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
