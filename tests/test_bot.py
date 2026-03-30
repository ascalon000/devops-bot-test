import pytest
from unittest.mock import Mock, AsyncMock
from src.telegram_bot import DevOpsBot

class TestDevOpsBot:
    
    def test_bot_initialization(self):
        bot = DevOpsBot("test_token")
        assert bot.token == "test_token"
        assert bot.application is not None
    
    @pytest.mark.asyncio
    async def test_start_command(self):
        bot = DevOpsBot("test_token")
        update = Mock()
        update.message = Mock()
        update.message.reply_text = AsyncMock()
        
        await bot.start_command(update, None)
        update.message.reply_text.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_help_command(self):
        bot = DevOpsBot("test_token")
        update = Mock()
        update.message = Mock()
        update.message.reply_text = AsyncMock()
        
        await bot.help_command(update, None)
        update.message.reply_text.assert_called_once()
    
    def test_send_notification_exists(self):
        bot = DevOpsBot("test_token")
        assert callable(bot.send_notification)
