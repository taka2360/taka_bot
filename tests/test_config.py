from pathlib import Path
import sys
from pathlib import Path as P

# テスト実行時にプロジェクトルートを sys.path に追加して local module をインポート可能にする
sys.path.insert(0, str(P.cwd()))

from bot import load_config


def test_load_config_default():
    # 存在しないファイルを渡して空 dict が返ることを確認
    cfg = load_config(Path("nonexistent_config.yaml"))
    assert isinstance(cfg, dict)
