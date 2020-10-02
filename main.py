import os
from os import urandom

from github import Github
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
TARGET_CHANNEL = os.getenv('TARGET_CHANNEL')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

github_client = Github(GITHUB_TOKEN)
client = discord.Client()

project_kingdoms_suggestions_repo = github_client.get_repo(
    'OutlawByteStudios/KingdomsDiscordBot')

suggestion_column = github_client.get_project_column(11079851)


#Suggestions project = 5594461
## Suggestions column = 11079851
#Project Plan project id = 5594457

suggestion_label = project_kingdoms_suggestions_repo.get_label('suggestion')

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

    suggestion = {}
    suggestion_parts = message.content.split('#')

    for part in suggestion_parts:
        if part.startswith('Title: '):
            suggestion['title'] = part[6:]
        elif part.startswith('Content: '):
            suggestion['content'] = part[8:]

    if not message.content.startswith('**Suggestion**') or 'title' not in suggestion or 'content' not in suggestion:
        dm_channel = await message.author.create_dm()
        await dm_channel.send('''Hey there, you posted something which did not have the correct format, please try again.\n
Remember that your suggestion should look like this:\n
\*\*Suggestion\*\*
#Title: Your Suggestion Title
#Content: Your Content\n
which can have\n
multiple lines\n______
\nHere is your original message:''')
        await dm_channel.send(message.content)
        await message.delete()
        return

    if 'title' in suggestion and 'content' in suggestion:
        suggestion['content'] += f'\n\n\n >🏰 Discord Suggestion from {message.author.name}@{message.author.id}'
        issue = project_kingdoms_suggestions_repo.create_issue(suggestion.get('title'), suggestion.get('content'), labels=[suggestion_label])
        suggestion_column.create_card(content_id = issue.id, content_type = 'Issue');
        title = suggestion.get('title').replace('\n', '');
        await message.channel.send(f'New suggestion from **{message.author.name}** ⚔: {title}!\nCheck it out at <https://github.com/orgs/OutlawByteStudios/projects/4>\nDirect Link: <{issue.html_url}>')
        await message.add_reaction('✅')
        dm_channel = await message.author.create_dm()
        await dm_channel.send(
f'''Hey there\n
Thanks for create adding suggestion! As soon as we can, we'll try to review your suggestion and let you know.\n
Here is the Link to your suggestion: {issue.html_url}
''')
        await message.delete()


client.run(TOKEN)
