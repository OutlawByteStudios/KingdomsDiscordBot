import nextcord
from src.defines import DISCORD_TOKEN

from nextcord.ext import commands


class SuggestModalView(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "New Suggestion",
            timeout=5 * 60,  # 5 minutes
        )

        self.suggestion_title = nextcord.ui.TextInput(
            label="Suggestion Title",
            min_length=2,
            max_length=50,
        )
        self.add_item(self.suggestion_title)

#remove this
        self.suggestion_topics = nextcord.ui.Select(
            placeholder="select one or more topics your suggestion is about",
            max_values=10,
            min_values=1,
            options=[
                nextcord.SelectOption(label='Crafting'),
                nextcord.SelectOption(label='Clans / Factions'),
                nextcord.SelectOption(label='Siege'),
                nextcord.SelectOption(label='Travel'),
                nextcord.SelectOption(label='Economy'),
                nextcord.SelectOption(label='Player Interaction'),
                nextcord.SelectOption(label='User Interface'),
                nextcord.SelectOption(label='Classes / Traits'),
                nextcord.SelectOption(
                    label='Interactables', description='Anything like carts, boats, ladders, bridges etc.'),
                nextcord.SelectOption(label='Not on this list'),
            ]
        )
        self.add_item(self.suggestion_topics)

        self.description = nextcord.ui.TextInput(
            label="Description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Describe your suggestion compact and simple, otherwise split into multiple suggestions",
            required=True,
            max_length=400,
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        response = f"New suggestion {self.suggestion_title.value} by {interaction.user.mention} [" + ', '.join(
            option for option in self.suggestion_topics.values) + "]"
        response += f"\n\n{self.description.value}"
        await interaction.send(response)


intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.slash_command(
    name="suggest",
    description="Post a new suggestion",
    guild_ids=[966368344037027901, 450652484634148875],
)
async def send(interaction: nextcord.Interaction):
    modal = SuggestModalView()
    await interaction.response.send_modal(modal)


bot.run(DISCORD_TOKEN)
