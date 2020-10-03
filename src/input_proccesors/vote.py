import re

class Vote:
    ___project_kingdoms_suggestions_repo = False

    VOTE_REGEX = "~upvote=(.*[0-9])\|downvote=(.*[0-9])"

    def __init__(self, repository) -> None:
        self.___project_kingdoms_suggestions_repo = repository

    async def process(self, message) -> None:
        parts = message.content.split(' ')
        user = message.author.name + '@' + str(message.author.discriminator)
        await message.delete()
        if len(parts) < 3:
                print('not enough arguments for voting')
                return
        issue_id = int(parts[1])
        rating = parts[2]

        voting_issue = self.___project_kingdoms_suggestions_repo.get_issue(
            number=issue_id)
        result = re.findall(
            self.VOTE_REGEX, voting_issue.title)
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
