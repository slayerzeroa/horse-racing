import asyncio
import telegram
import tools

token, chat_id = tools.get_env('TELEGRAM')

async def main():
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text='테스트 메세지', chat_id=chat_id)

# pandas dataframe to string
def df_to_str(df):
    return df.to_string()


async def send_df(df):
    bot = telegram.Bot(token)
    async with bot:
        await bot.send_message(text=df_to_str(df), chat_id=chat_id)

#
# if __name__ == '__main__':
#     asyncio.run(main())