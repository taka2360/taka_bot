import os
import logging
from pathlib import Path
from typing import Dict, Any, List

import yaml
from dotenv import load_dotenv
import discord
from discord.ext import commands

# ロギング設定
logger = logging.getLogger("taka_bot")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
logger.addHandler(handler)


def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        logger.warning("config.yaml が見つかりません。デフォルト値を使用します。")
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class ExtensibleBot(commands.Bot):
    def __init__(self, config: Dict[str, Any]):
        intents = discord.Intents.default()
        # デフォルトで message_content を無効にしている discord.py のバージョンがあるため、設定で上書き
        intents.message_content = config.get("intents", {}).get("message_content", False)

        prefix = config.get("command_prefix", "!")
        application_id = config.get("application_id")

        super().__init__(command_prefix=prefix, intents=intents, application_id=application_id)
        self.config = config
        self.cogs_path = Path(config.get("cogs_path", "cogs"))

    async def setup_hook(self) -> None:
        # setup_hook は Bot が起動する前に呼ばれるのでここで Cog をロード
        await self.load_all_cogs()

    def find_cogs(self) -> List[str]:
        """cogs ディレクトリ内の拡張モジュール名を dotted path 形式で返す"""
        base = Path.cwd() / self.cogs_path
        if not base.exists():
            logger.warning("cogs ディレクトリが存在しません: %s", str(base))
            return []
        cogs: List[str] = []
        for p in base.rglob("*.py"):
            if p.name.startswith("__"):
                continue
            # cogs/example.py -> cogs.example
            rel = p.relative_to(Path.cwd()).with_suffix("")
            dotted = ".".join(rel.parts)
            cogs.append(dotted)
        return sorted(cogs)

    async def load_all_cogs(self) -> None:
        cogs = self.find_cogs()
        logger.info("Found cogs: %s", cogs)
        for ext in cogs:
            try:
                logger.info("Loading extension: %s", ext)
                await self.load_extension(ext)
            except Exception as e:
                logger.exception("Failed to load extension %s: %s", ext, e)

    async def on_ready(self) -> None:
        logger.info("Logged in as %s (id=%s)", self.user, self.user.id)


def main() -> None:
    # .env をロードして環境変数を上書き
    load_dotenv()

    config_path = Path.cwd() / "config.yaml"
    config = load_config(config_path)

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("環境変数 DISCORD_TOKEN が設定されていません。終了します。")
        return

    bot = ExtensibleBot(config)
    bot.run(token)


if __name__ == "__main__":
    main()
