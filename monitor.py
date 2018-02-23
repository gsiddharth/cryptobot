import arbitrage
from telegram.ext import Updater, CommandHandler
import time
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class Monitor:

    def __init__(self, params, default_threshold):        
        self.params = params
        self.default_threshold = default_threshold
        self.user_thresholds = {}
        self.last_published = {}
    
    def arb(self, bot, update, args):
        try:
            threshold = self.default_threshold            

            if(len(args) == 1):
                threshold = float(args[0])

            user = update.message.from_user   
            self.user_thresholds[user.id] = threshold            

            print("Publishing arbitrage updates to " + str(user.id) + " with threshold > " + str(threshold))
            update.message.reply_text("Publishing arbitrage updates with threshold > " + str(threshold))

        except Exception as E:
            print(E)

    def monitor(self, bot, update):
        try:
            for user_id, threshold in self.user_thresholds.items():                                
                arbs = {}
                txt = ""
                
                published = ""
            
                for k, val in self.params.items():                
                    arb = arbitrage.arbitrage(val[0], val[1], val[2], val[3], val[4])
                    if(arb[0] > threshold or arb[1] > threshold):
                        arbs[k] =  arb
                        if(arb[0] > threshold):
                            txt += k + "\t\t\t\t<b>" + str(arb[0]) + "</b>\t\t\t\t" + str(arb[1]) + "\n"
                        if(arb[1] > threshold):
                            txt += k + "\t\t\t\t" + str(arb[0]) + "\t\t\t\t<b>" + str(arb[1]) + "</b>\n"

                        published += k + ":"

                if(txt != ""):                    
                    if(user_id not in self.last_published or self.last_published[user_id] != published):
                        bot.sendMessage(chat_id = user_id, text = txt, parse_mode = "html")
                        self.last_published[user_id] = published
                else:                    
                    if(user_id not in self.last_published or self.last_published[user_id] != published):                        
                        bot.sendMessage(chat_id = user_id, text = "No arbitrage")
                        self.last_published[user_id] = published

        except Exception as E:
            print(E)        

    def stop(self, bot, update):
        try:
            user_id = update.message.from_user.id

            if(user_id in self.user_thresholds):
                del self.user_thresholds[user_id]
                
            update.message.reply_text("Stopped arbitrage updates")
            print("Stopped arbitrage updates to " + str(user_id))

        except Exception as E:
            print(E)
        

param_list = {"BCHETH" : ["koinex", "bitfinex", "BCH", "ETH", "BCHETH"],
    "BCHBTC" : ["koinex", "bitfinex", "BCH", "BTC", "BCHBTC"],
    "ETHBTC" : ["koinex", "bitfinex", "ETH", "BTC", "ETHBTC"],
    "XRPBTC" : ["koinex", "bitfinex", "XRP", "BTC", "XRPBTC"],
    "LTCBTC" : ["koinex", "bitfinex", "LTC", "BTC", "LTCBTC"],
    "OMGBTC" : ["koinex", "bitfinex", "OMG", "BTC", "OMGBTC"],
    "OMGETH" : ["koinex", "bitfinex", "OMG", "ETH", "OMGETH"]}

monitor = Monitor(param_list, 0)

updater = Updater('517487463:AAHQc1nko2re_n0Qww-fSKoIN_aHerCbTwQ')

updater.dispatcher.add_handler(CommandHandler('arb', monitor.arb, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('stop', monitor.stop))

j = updater.job_queue
job_minute = j.run_repeating(monitor.monitor, 30, 0)
updater.start_polling()
updater.idle