# Reddit Groq Bot

A Reddit bot that automatically generates and posts content using Groq AI, with the ability to make intelligent comments on existing posts.

## Features

- 🤖 AI-powered content generation using Groq API
- 📝 Automated daily posting at scheduled times
- 💬 Intelligent commenting on relevant posts
- 🔄 Rate limiting and error handling
- 📊 Comprehensive logging system

## Prerequisites

- Python 3.8+
- Reddit account
- Reddit API credentials
- Groq API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-groq-bot.git
cd reddit-groq-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your credentials:
```env
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT="python:yourbotname:v1.0 (by /u/yourusername)"
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password
GROQ_API_KEY=your_groq_api_key
TARGET_SUBREDDIT=target_subreddit_name
```

## Getting API Credentials

### Reddit API Credentials
1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the following:
   - Name: Your bot's name
   - Select "script"
   - Redirect URI: http://localhost:8080
4. Note down the client_id and client_secret

### Groq API Key
1. Sign up at https://console.groq.com
2. Generate an API key from your dashboard
3. Copy the key to your `.env` file

## Usage

Run the bot:
```bash
python bot.py
```

The bot will:
- Post daily at 10:00 AM (configurable)
- Comment on relevant posts every 4 hours
- Log activities to `reddit_bot.log`

## Configuration

### Posting Schedule
Modify the schedule in `main()`:
```python
schedule.every().day.at("10:00").do(bot.run_scheduled_post)
schedule.every(4).hours.do(bot.comment_on_posts)
```

### Comment Criteria
Adjust post selection criteria in `should_comment_on_post()`:
```python
def should_comment_on_post(self, post):
    return (
        post.id not in self.commented_posts and
        post.score > 5 and
        len(post.comments) < 50 and
        post.created_utc > (time.time() - 86400)
    )
```

### Content Generation
Modify the prompts in:
- `generate_content()` for posts
- `generate_comment()` for comments

## Logging

Logs are written to `reddit_bot.log` with the following information:
- Successful posts and comments
- Error messages
- Schedule execution
- API interaction issues

## Safety Features

- Rate limiting between actions
- Error handling and recovery
- Duplicate comment prevention
- Activity logging
- Secure credential management

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational purposes. Make sure to follow Reddit's API terms of service and bot guidelines when using this code.

## Support

If you encounter any issues or have questions, please open an issue in the GitHub repository.
