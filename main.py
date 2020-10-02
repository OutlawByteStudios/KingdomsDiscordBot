import os
from os import urandom

from github import Github
import discord
from dotenv import load_dotenv
import re

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


# Suggestions project = 5594461
# Suggestions column = 11079851
# Project Plan project id = 5594457

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
    if message.content.startswith('!vote'):
        parts = message.content.split(' ')
        user = message.author.name + '@' + str(message.author.discriminator)
        await message.delete()
        if len(parts) < 3:
            print('not enough arguments for voting')
            return
        issue_id = int(parts[1])
        rating = parts[2]

        voting_issue = project_kingdoms_suggestions_repo.get_issue(
            number=issue_id)


        result = re.findall(
            "~upvote=(.*[0-9])\|downvote=(.*[0-9])", voting_issue.title)

        upvotes = int(result[0][0])
        downvotes = int(result[0][1])
        comments = voting_issue.get_comments()

        if rating in ['up', '+', 'upvote', 'yes']:
            for comment in comments:
                if user in comment.body and '+' in comment.body:
                    print('already voted up')
                    return
            voting_issue.create_comment(f'user {user} voted +')
            upvotes += 1
        elif rating in ['down', '-', 'downvote', 'no']:
            for comment in comments:
                if user in comment.body and '-' in comment.body:
                    print('already voted down')
                    return
            voting_issue.create_comment(f'user {user} voted -')
            downvotes += 1

        original_title = voting_issue.title.split('~')[0]
        new_title = original_title + f'~upvote={upvotes}|downvote={downvotes}'
        voting_issue.edit(title=new_title)
        return
    else:
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
            suggestion['content'] += f'\n\n\n >🏰 Discord Suggestion from {message.author.name}@{message.author.discriminator}'
            title_plain = suggestion['title']
            suggestion['title'] += f' ~upvote=0|downvote=0'
            issue = project_kingdoms_suggestions_repo.create_issue(suggestion.get(
                'title'), suggestion.get('content'), labels=[suggestion_label])
            suggestion_column.create_card(
                content_id=issue.id, content_type='Issue')
            title = title_plain.replace('\n', '')
            await message.channel.send(
f'''New suggestion from **{message.author.name}** ⚔: {title}!\n
Don't forget to vote!
**Up Vote:** ```!vote {issue.number} +```
**Down Vote:** ```!vote {issue.number} -```
\n
Check it out at <https://github.com/orgs/OutlawByteStudios/projects/4>\r
Direct Link: <{issue.html_url}>''')
            await message.add_reaction('✅')
            dm_channel = await message.author.create_dm()
            await dm_channel.send(
                f'''Hey there\n
Thanks for adding a suggestion! As soon as we can, we'll try to review your suggestion and let you know.\n
Here is the Link to your suggestion: {issue.html_url}
''')
            await message.delete()


client.run(TOKEN)
