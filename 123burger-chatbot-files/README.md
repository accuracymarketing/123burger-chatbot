# 123Burger Customer Chatbot

A small Python chatbot for answering common restaurant customer questions. It can run in the terminal or as a website chat widget.

The bot is configured for **123Burger** in Raleigh, NC, and can answer questions about:

- Hours
- Location and parking
- Burgers and popular menu items
- Chicken, fries, and shakes
- Halal and freshness information
- Dietary options and allergies
- Takeout and delivery
- Contact information
- The mobile app
- Kids and family seating

Verified restaurant details currently used by the bot:

- Address: 4150 Fayetteville Rd, Raleigh, NC 27603
- Phone: (+1) 919-679-7400
- Email: 123burgernc@gmail.com
- Ordering link: https://www.123burger.com/menu

The menu and hours were copied from the public 123Burger website. Check the live site before publishing if prices or hours change.

## Run the chatbot

```bash
python3 restaurant_chatbot.py
```

Type a question like:

```text
Do you take reservations?
What time do you close on Friday?
What burgers do you have?
Are you halal?
How much are fries?
```

Type `quit` to leave.

## Run the website demo

```bash
python3 web_chatbot.py
```

Then open:

```text
http://127.0.0.1:8000
```

The demo page loads `static/chatbot-widget.js`, which adds a chat button to the bottom-right corner of the page.

## Deploy on Render

Create a **Web Service**, not a Private Service.

Use these settings:

- Runtime: Python
- Build command: leave blank or use `pip install -r requirements.txt`
- Start command: `python web_chatbot.py`

Render will provide a public URL after deployment. Use that URL in your website embed code.

## Add it to an existing website

1. Put `chatbot-widget.js` on your website.
2. Run `web_chatbot.py` on a server so the website can call the `/chat` endpoint.
3. Add this before the closing `</body>` tag on your restaurant website:

```html
<script>
  window.RestaurantChatbotApi = "https://your-domain.com/chat";
</script>
<script src="https://your-domain.com/chatbot-widget.js"></script>
```

For local testing, use:

```html
<script src="http://127.0.0.1:8000/chatbot-widget.js"></script>
```

## Run tests

```bash
python3 -m unittest
```

The chatbot uses a simple keyword and fuzzy-matching approach, so it works offline and does not require an API key or third-party packages.
