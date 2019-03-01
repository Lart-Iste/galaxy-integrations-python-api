import asyncio
import json

from galaxy.api.types import Achievement
from galaxy.api.errors import UnknownError

def test_success(plugin, readline, write):
    request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "import_unlocked_achievements",
        "params": {
            "game_id": "14"
        }
    }
    readline.side_effect = [json.dumps(request), ""]
    plugin.get_unlocked_achievements.return_value = [
        Achievement("lvl10", 1548421241),
        Achievement("lvl20", 1548422395)
    ]
    asyncio.run(plugin.run())
    plugin.get_unlocked_achievements.assert_called_with(game_id="14")
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "3",
        "result": {
            "unlocked_achievements": [
                {
                    "achievement_id": "lvl10",
                    "unlock_time": 1548421241
                },
                {
                    "achievement_id": "lvl20",
                    "unlock_time": 1548422395
                }
            ]
        }
    }

def test_failure(plugin, readline, write):
    request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "import_unlocked_achievements",
        "params": {
            "game_id": "14"
        }
    }

    readline.side_effect = [json.dumps(request), ""]
    plugin.get_unlocked_achievements.side_effect = UnknownError()
    asyncio.run(plugin.run())
    plugin.get_unlocked_achievements.assert_called()
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "id": "3",
        "error": {
            "code": 0,
            "message": "Unknown error"
        }
    }

def test_unlock_achievement(plugin, write):
    achievement = Achievement("lvl20", 1548422395)

    async def couritine():
        plugin.unlock_achievement("14", achievement)

    asyncio.run(couritine())
    response = json.loads(write.call_args[0][0])

    assert response == {
        "jsonrpc": "2.0",
        "method": "achievement_unlocked",
        "params": {
            "game_id": "14",
            "achievement": {
                "achievement_id": "lvl20",
                "unlock_time": 1548422395
            }
        }
    }