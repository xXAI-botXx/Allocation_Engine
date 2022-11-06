import os

import pywhatkit as whatsapp

numb = str(os.environ["number"])

whatsapp.sendwhatmsg(numb, "Message 2", 18, 55, 15, True, 2)

