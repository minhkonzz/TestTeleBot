import json
from operator import itemgetter
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

json_data = open('keys.json')
keys = json.load(json_data)
json_data.close()
api_id, api_hash, bot_token = itemgetter('api_id', 'api_hash', 'bot_token')(keys)

bot = TelegramClient('get_usersname_bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage)
async def handle_user_message(event):
   sender = await event.get_sender()
   if event.text == '/start':
      await event.reply('Xin chào @' + str(sender.username) + ', hãy nhập vào link telegram của group mà bạn muốn lấy danh sách username')
      return
   try:
      group = await bot.get_entity(event.text)
      mems_count = 0
      nones = 0
      offset = 0
      while True:
         list_mems_str = ''
         result = await bot(GetParticipantsRequest(group, ChannelParticipantsSearch(''), offset, 120, hash=0))
         users_fetched = result.users
         if not users_fetched:
            break
         for user in users_fetched:
            if user.username is None:
               nones += 1
               continue
            mems_count += 1
            list_mems_str += str(mems_count) + '. @' + str(user.username) + '\n'
         await bot.send_message(sender, list_mems_str)
         offset += len(users_fetched)
      await bot.send_message(sender, 'Hoàn tất. Có ' + str(nones) + ' user không đặt username')
   except:
      await event.reply(
         'Không thể lấy danh sách username. Kiểm tra lại 1 trong những nguyên nhân sau:\n' +
         '1. Link group không hợp lệ\n' +
         '2. Link group đã private hoặc hết phiên truy cập\n' +
         '3. Số lượng user quá lớn (> 10000 members)'
      )

def main():
   bot.run_until_disconnected()

if __name__ == '__main__':
   main()

