//+------------------------------------------------------------------+
//|                                                      DummyBot.mq5|
//|         Simulates a trading bot with periodic API checks         |
//+------------------------------------------------------------------+
#property script_show_inputs

input string api_base = "http://localhost:5000/api/bots";
input string bot_id = "YOUR_BOT_ID_HERE"; // Set your bot's bot_id here

datetime last_check = 0;
int check_interval = 30; // seconds

int OnInit()
  {
   Print("DummyBot started. bot_id=", bot_id);
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
   Print("DummyBot stopped.");
  }

void OnTick()
  {
   if(TimeCurrent() - last_check >= check_interval)
     {
      last_check = TimeCurrent();
      Print("[DummyBot] Tick at ", TimeToString(TimeCurrent(), TIME_SECONDS), ", checking validity and state...");
      CheckValidity();
      CheckBotState();
     }
  }

void CheckValidity()
  {
   string url = api_base + "/check_validity";
   string headers = "Content-Type: application/json\r\n";
   string body = "{\"bot_id\":\"" + bot_id + "\"}";
   uchar post[];
   StringToCharArray(body, post);
   uchar result[];
   string headers_out;
   int timeout = 5000;
  string cookie = "";
  int res = WebRequest("POST", url, cookie, headers, timeout, post, ArraySize(post)-1, result, headers_out);
   if(res == 200)
     {
      string response = CharArrayToString(result);
      Print("Validity response: ", response);
      if(StringFind(response, "\"valid\":false") >= 0)
        {
         Print("Bot is not valid. Stopping trading.");
         // Add logic to stop trading here
        }
     }
   else
     {
      Print("Validity check failed. Error code: ", GetLastError());
     }
  }

void CheckBotState()
  {
  string url = api_base + "?bot_id=" + bot_id;
  uchar empty[];
  uchar result[];
  string headers_out;
  int timeout = 5000;
  string cookie = "";
  int res = WebRequest("GET", url, cookie, "", timeout, empty, 0, result, headers_out);
  if(res == 200)
    {
    string response = CharArrayToString(result);
    Print("Bot details: ", response);
    // Simple parsing (for demo): look for "bot_state" and "hard_stop_all_trades"
    bool bot_state = (StringFind(response, "\"bot_state\":true") >= 0);
    bool hard_stop = (StringFind(response, "\"hard_stop_all_trades\":true") >= 0);
    if(!bot_state)
      Print("Bot state is OFF. Should stop trading.");
    if(hard_stop)
      Print("Hard stop is ON. Should close all trades and stop.");
    // Add your trading logic here
    }
  else
    {
    Print("Bot state check failed. Error code: ", GetLastError());
    }
  }
