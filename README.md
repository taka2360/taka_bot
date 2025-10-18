# Discord Bot (discord.py) — 拡張性の高いテンプレート

このリポジトリは、拡張性を重視した discord.py ベースの Discord ボット雛形です。

主要ファイル:
- `bot.py` : エントリーポイント。設定読み込み、拡張（Cog）の動的ロード、ロギングを含む。
- `cogs/example.py` : サンプル Cog（`ping` コマンドなど）。
- `config.yaml` : 設定ファイル（例）。

セットアップ（Windows PowerShell）:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

実行:
- 環境変数 `DISCORD_TOKEN` に Bot トークンを設定するか、プロジェクトルートの `.env` に `DISCORD_TOKEN=...` を置いてください。

```powershell
python bot.py
```

セキュリティ:
- トークンは絶対に公開しないでください。`.env` や `config.yaml` をリポジトリにコミットしないよう `.gitignore` を確認してください。

拡張:
- `cogs/` 以下に Cog を追加してください。自動で検出してロードします。
