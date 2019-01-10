# Configuration

## config.ini

 **Default**
 
 * `starting_currency` Newly created accounts start with this amount of 
 currency
 * `currency_name` The name of the currency the bot refers to and some of the
  useable commands
  
  **Bot**
  
  * `cooldown` How frequently the bot can handle commands. The commands do 
  not get queued, they will be ignored
  
  **Mongodb**
  
  * `ip` ip address of the mongodb instance. Default `localhost`
  * `port` port that the mongodb instance uses. Default `27017`
  
  **Slots**
  
  * `slot_price` The cost in currency it is to use the command `!slots`. 
  Default `5`
  * `num_reels` The number of reels to spin in the slot game. Default `3`
  * `jackpot_multiplier` Multiplies the payout amount for getting all reels 
  the same emote. Default `2`
  * `multiplier` Multiplies the payout. Default `1`
  * `user_slots_freq` How frequently a user is allowed to play `!slots` in 
  seconds. Default `120`
  
  **Guess**
  
  * `payout` How much currency to award a player for guessing the correct 
  number. Default `50`
  * `consolation_prize` If the guess is within +- 2 of the true number, award
   the player with the consolation prize in currency. Default `5`
  * `max_guess` The max guess allowed in the guessing game. 
   Default `100`
  * `bot_win_cooldown` When someone guesses the correct number, no one will 
  be able to play for this amount of seconds. Default `180`
  * `user_guess_cooldown` How frequently a user can use the `!guess` command 
  in seconds. Default `30`
  
  **Trickle**
  
  * `trickle` The amount in currency to trickle to users. Default `1`
  * `frequency` How often to trickle users in seconds. Default `600`
  
  **Dice**
  
  * `dice_enabled` Allows users to use the command `!roll`. Default `true`
  * `max_roll` Highest number you can roll. 1-max_roll. Default `6`
  
  **Commands**
  
  * `user_cmd_cooldown` How frequently a user can use any command in seconds. 
  Default `5`
  
  **Twitch**
  
  * `server` The server the irc bot will connect to. Default `irc.chat.twitch.tv`
  * `port` The port the bot will use for the server. Default `6667` 
  
 ## credentials.ini
 
 * `BOT_NAME` The account to log into Twitch.tv
 * `CLIENT_ID` The account's client_id
 * `OAUTH` The account's oauth
 * `CHANNEL` The channel for the bot to join and monitor