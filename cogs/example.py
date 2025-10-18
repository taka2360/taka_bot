from discord.ext import commands


class Example(commands.Cog):
    """サンプル Cog: ping コマンドと on_ready のログを含む"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Cog の on_ready は Bot の on_ready と同時に呼ばれる
        if self.bot.user:
            print(f"Example Cog loaded for {self.bot.user}")

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """ボットのレイテンシを返す"""
        latency_ms = round(self.bot.latency * 1000)
        await ctx.reply(f"Pong! {latency_ms}ms")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Example(bot))
