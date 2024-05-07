#scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import db
from models import Post

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_post_publish(post_id, publish_time):
    """Task to publish a post."""
    def publish():
        post = Post.query.get(post_id)
        if post:
            post.published = True
            db.session.commit()

    scheduler.add_job(publish, 'date', run_date=publish_time)
