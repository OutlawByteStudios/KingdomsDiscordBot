class Suggestion:

    ___WRONG_FORMAT_RESPONSE = '''Hey there, you posted something which did not have the correct format, please try again.\n
Remember that your suggestion should look like this:\n
\*\*Suggestion\*\*
#Title: Your Suggestion Title
#Content: Your Content\n
which can have\n
multiple lines\n______
\nHere is your original message:'''

    ___project_kingdoms_suggestions_repo = False
    ___suggestion_column = False
    ___suggestion_label = False

    def __init__(self, repository, column, label) -> None:
        self.___project_kingdoms_suggestions_repo = repository
        self.___suggestion_column = column
        self.___suggestion_label = label
        pass

    async def process(self, message):
        suggestion = {}
        suggestion_parts = message.content.split('#')

        for part in suggestion_parts:
            if part.startswith('Title: '):
                suggestion['title'] = part[6:]
            elif part.startswith('Content: '):
                suggestion['content'] = part[8:]

        if not message.content.startswith('**Suggestion**') or 'title' not in suggestion or 'content' not in suggestion:
            dm_channel = await message.author.create_dm()
            await dm_channel.send(self.___WRONG_FORMAT_RESPONSE)
            await dm_channel.send(message.content)
            await message.delete()
            return

        if 'title' in suggestion and 'content' in suggestion:
            suggestion['content'] += f'\n\n\n >🏰 Discord Suggestion from {message.author.name}@{message.author.discriminator}'
            title_plain = suggestion['title']
            suggestion['title'] += f' ~upvote=0|downvote=0'
            issue = self.___project_kingdoms_suggestions_repo.create_issue(suggestion.get(
                'title'), suggestion.get('content'), labels=[self.___suggestion_label])
            self.___suggestion_column.create_card(
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