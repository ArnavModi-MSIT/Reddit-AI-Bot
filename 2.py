import praw
import groq
import schedule
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

logging.basicConfig(
    filename='reddit_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

class RedditGroqBot:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD')
        )
        self.groq_client = groq.Client(api_key=os.getenv('GROQ_API_KEY'))
        self.subreddit_name = os.getenv('TARGET_SUBREDDIT')
        self.subreddit = self.reddit.subreddit(self.subreddit_name)
        self.commented_posts = set()

    def generate_content(self):
        try:
            prompt = """Generate an engaging Reddit post about a fascinating science fact. 
            Include a catchy title and detailed explanation. Format the response as:
            Title: [title here]
            Content: [content here]"""
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=500
            )
            response = completion.choices[0].message.content
            lines = response.split('\n')
            title = lines[0].replace('Title:', '').strip()
            content = '\n'.join(lines[2:]).replace('Content:', '').strip()
            return title, content
        except Exception as e:
            logging.error(f"Error generating content: {str(e)}")
            return None, None

    def generate_comment(self, post_title, post_content):
        try:
            prompt = f"""Generate a thoughtful and relevant Reddit comment for the following post:
            Title: {post_title}
            Content: {post_content}
            
            The comment should be:
            1. Relevant to the post topic
            2. Add value to the discussion
            3. Be engaging but not controversial
            4. Include relevant information or insights
            
            Generate only the comment text without any additional formatting."""
            completion = self.groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=300
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            logging.error(f"Error generating comment: {str(e)}")
            return None

    def should_comment_on_post(self, post):
        return (
            post.id not in self.commented_posts and
            post.created_utc > (time.time() - 86400)
        )

    def comment_on_posts(self, limit=10):
        try:
            for post in self.subreddit.new(limit=limit):
                if self.should_comment_on_post(post):
                    comment_text = self.generate_comment(post.title, post.selftext)
                    if comment_text:
                        comment = post.reply(comment_text)
                        self.commented_posts.add(post.id)
                        logging.info(f"Commented on post {post.id}: {comment.id}")
                        time.sleep(30)
        except Exception as e:
            logging.error(f"Error in comment_on_posts: {str(e)}")

    def make_post(self):
        try:
            title, content = self.generate_content()
            if title and content:
                submission = self.subreddit.submit(title=title, selftext=content)
                logging.info(f"Successfully posted to Reddit: {submission.url}")
                return True
            else:
                logging.error("Failed to generate content")
                return False
        except Exception as e:
            logging.error(f"Error posting to Reddit: {str(e)}")
            return False

    def run_scheduled_post(self):
        logging.info("Running scheduled post")
        success = self.make_post()
        if success:
            logging.info("Scheduled post completed successfully")
        else:
            logging.error("Scheduled post failed")

def main():
    bot = RedditGroqBot()
    schedule.every().day.at("12:03").do(bot.run_scheduled_post)
    schedule.every().day.at("12:03").do(bot.comment_on_posts)
    logging.info("Bot started successfully")
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except Exception as e:
            logging.error(f"Error in main loop: {str(e)}")
            time.sleep(300)

if __name__ == "__main__":
    main()
