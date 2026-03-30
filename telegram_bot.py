import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class DevOpsBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(token).build()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_message = """
*Devops Pipeline Bot*

*Доступные команды:*
/start - Показать приветствие
/help - Показать справку

Бот автоматически отправляет уведомления о новых релизах
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
*Справка по использованию*

*Автоматические уведомления:*
• При создании Pull Request
• При мерже веток
• При создании релиза

*Формат уведомлений:*
• Название проекта
• Версия релиза
• Ветка и время мержа
• Ссылки на GitHub
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def send_notification(self, chat_id: str, release_info: dict):
        message = f"""
*НОВЫЙ ВЫПУСК ИЗМЕНЕНИЙ*

*Проект:* `{release_info.get('project', 'devops_bot')}`
*Версия:* `{release_info.get('version', 'unknown')}`
*Дата:* `{release_info.get('date', 'N/A')}`
*Ветка:* `{release_info.get('branch', 'feature/ticket-***')} → dev`
*Ссылка на мерж:* [Посмотреть Pull Request]({release_info.get('pr_url', '#')})

*Информация о Git-репозитории*
[Открыть репозиторий]({release_info.get('repo_url', '#')})
*GIT TAG:* `{release_info.get('tag', 'N/A')}`

*Информация о Docker-репозитории*
*Владелец:* `{release_info.get('owner', 'N/A')}`
*Название:* `{release_info.get('repo_name', 'N/A')}`
*Полное имя:* `{release_info.get('docker_full_name', 'N/A')}`

*Качество кода:*
        """

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Посмотреть Pipeline", url=release_info.get('pipeline_url', '#')),
             InlineKeyboardButton("📝 Смотреть изменения", url=release_info.get('pr_url', '#'))]
        ])

        await self.application.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
        logger.info(f"Notification sent to chat {chat_id}")

    def run(self):
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        logger.info("Bot is starting...")
        self.application.run_polling()


if __name__ == '__main__':
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable is not set")
        exit(1)

    bot = DevOpsBot(token)
    bot.run()
    
