import discord, os, keep_alive, asyncio, datetime, pytz, re, requests

from colorama import Fore
from discord.ext import commands

class disClient(commands.Bot):
  def __init__(self):
    super().__init__(
      command_prefix=':',
      self_bot=True
    )

    
    self.session = requests.Session()
    self.token = os.getenv("TOKEN")
    self.remove_command('help')
    self.errors = {
      1: '{"message": "Unknown Gift Code", "code": 10038}',
      2: '{"message": "This gift has been redeemed already.", "code": 50050}',
      3: 'You are being rate limited',
      4: 'Access denied'
    }

#Redeem
  async def on_message(self, message):
    try:
      code = re.search(r'(discord.gift|discordapp.com/gifts)/\w{16,24}', message.content).group(0)
      if code:
        payload = {
          'channel_id': None,
          'payment_source_id': None
        }

    
        r = self.session.post(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code.replace("discord.gift/", "")}/redeem', headers=self.getHeaders(), json=payload)
        if self.errors[1] in r.text:
          self.returnData('INVALID CODE', code, message.guild, message.author)
          self.Save('log.txt', 'a+', f'[WARN] Invalid Code {code} | {message.guild} | {message.author}')
        elif self.errors[2] in r.text:
          self.returnData('ALREADY REDEEMED', code, message.guild, message.author)
          self.Save('log.txt', 'a+', f'[INFO] Already redeemed Code {code} | {message.guild} | {message.author}')
        elif self.errors[3] in r.text:
          self.returnData('RATELIMITED', code, message.guild, message.author)
          self.Save('log.txt', 'a+', '[WARN] RateLimited')
        elif self.errors[4] in r.text:
          self.returnData('DENIED', code, message.guild, message.author)
          self.Save('log.txt', 'a+', '[WARN] Denied')
        else:
          self.returnData('CLAIMED', code, message.guild, message.author)
          self.Save('log.txt', 'a+', f'[INFO] Claimed Code {code} | {message.guild} | {message.author} | {r.text}')
    except (AttributeError):
      pass







  def returnData(self, status, code, value1, value2):
    if status == 'INVALID CODE' or 'DENIED':
      perhaps = Fore.RED
    elif status == 'ALREADY REDEEMED' or 'RATELIMITED' or 'UNKNOWN':
      perhaps = Fore.YELLOW
    else:
      perhaps = Fore.GREEN
    data = print(f'[{perhaps}{status}{Fore.RESET}] - [{Fore.CYAN}{code}{Fore.RESET}] - [{Fore.YELLOW}{value1}{Fore.RESET}] - [{Fore.YELLOW}{value2}{Fore.RESET}]')
    return data

  def getHeaders(self):
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36',
      'Authorization': self.token
    }
    return headers

  def Save(self, fileName, mode, info):
    return open(fileName, mode).write(info+'\n')

  def run(self):
    super().run(self.token, bot=False)














    

if __name__ == '__main__':
  client = disClient()
  keep_alive.keep_alive()
  client.run()
