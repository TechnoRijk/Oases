#routes.py
from sqlalchemy import desc
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from datetime import datetime, time
from forms import RegistrationForm
from flask_socketio import SocketIO, emit
from flask_limiter.util import get_remote_address
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import jsonify, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from oases import app, db
from oases import app, db
from models import User
from models import User
import openai

# Initialize Flask app
app = app
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
bcrypt = Bcrypt(app)

# Register Flask-Uploads for image uploading
images = UploadSet('images', IMAGES)
app.config['UPLOADED_IMAGES_DEST'] = 'path/to/your/uploaded/images'
configure_uploads(app, images)

# Initialize Flask-Limiter with appropriate key_func
bcrypt = Bcrypt(app)
limiter = Limiter(
    get_remote_address,
    app=app,
)

# Function to fetch posts from RSS feed
def fetch_rss_posts(feed_url):
    posts = feedparser.parse(feed_url)
    for post in posts.entries:
        new_post = Post(title=post.title, summary=post.summary, published_date=datetime.strptime(post.published, '%Y-%m-%dT%H:%M:%SZ'))
        db.session.add(new_post)
    db.session.commit()

#### ==== App Routes === ###

# Define routes
@app.route('/')
def index():
    return render_template('dashboard.html')

# Route to serve the dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
    
## ------- logins ------ ##

# Enhanced login route with security features
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # No need to sanitize here if you're using SQLAlchemy
        # Perform login logic
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')

# Logout route
@app.route('/user/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})


# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user based on form data
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))  # Redirect to login page after successful registration
    return render_template('register.html', form=form)

   # Function to hash a password
def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8') 


## ------ post and schedule ------ ##

scheduler = BackgroundScheduler()

# Define the schedule_post function
def schedule_post(post_id):
    # Placeholder for actual scheduling logic
    print(f"Post {post_id} scheduled")

# Define the days and times for scheduling
days = ['mon', 'tue', 'thu']
times = [time(16, 0)] * len(days)  # Scheduled at 16:00

# For Friday, schedule at 18:00
days.append('fri')
times.append(time(18, 0))

# Schedule the posts
for day, time in zip(days, times):
    scheduler.add_job(schedule_post, 'cron', day_of_week=day, hour=time.hour, minute=time.minute, args=['your_post_id'])

# Route for rewriting and scheduling posts
@app.route('/posts/rewrite', methods=['POST'])
@login_required
def rewrite_post():
    post_id = request.form['post_id']
    new_content = request.form['content']
    tone = request.form['tone']
    style = request.form['style']
    length = request.form['length']
    promotional = request.form['promotional']
    
    # Update the post details
    post = Post.query.get(post_id)
    post.content = new_content  # Assuming content modification is handled here
    db.session.commit()

    # Simulate scheduling logic
    schedule_post(post_id)
    return jsonify({'message': 'Post rewritten and scheduled successfully!'}), 200


## ------ RSS Feed ------ ##

# Schedule fetching posts from RSS feeds on specific days
scheduler.add_job(func=fetch_rss_posts, trigger='cron', day_of_week='mon,thu,sun', args=['http://example.com/feed'])

# Route to fetch and summarize articles
@app.route('/fetch_articles', methods=['GET'])
def fetch_articles():
    topics = ['proptech', 'tokenization', 'cryptocurrency in property', 'co-ownership in property']
    articles = []
    for topic in topics:
        # Placeholder for fetching articles from an external API
        response = requests.get(f'http://example.com/api/articles?topic={topic}')
        if response.status_code == 200:
            articles.extend(response.json()['articles'])
    return jsonify({'articles': articles})



# Route to add an RSS feed
@app.route('/rss/add', methods=['POST'])
@login_required
def add_rss_feed():
    feed_url = request.form['url']
    new_feed = RSSFeed(url=feed_url)
    db.session.add(new_feed)
    db.session.commit()
    return jsonify({'message': 'RSS feed added successfully!'}), 200

# Route to remove an RSS feed
@app.route('/rss/remove', methods=['POST'])
@login_required
def remove_rss_feed():
    feed_id = request.form['id']
    feed_to_remove = RSSFeed.query.get(feed_id)
    db.session.delete(feed_to_remove)
    db.session.commit()
    return jsonify({'message': 'RSS feed removed successfully!'}), 200


## ------ Image generation ------ ##

# Create image route
app.route('/user/create-image', methods=['POST'])
@login_required
def create_image():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'message': 'Prompt is required'}), 400
    
    try:
        # Retrieve the OpenAI API key from the environment variable
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            return jsonify({'message': 'OpenAI API key not found'}), 500
        
        # Make an API call to DALL-E to generate an image based on the prompt
        dall_e_api_url = "https://api.openai.com/v1/images/generations"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}'
        }
        data = {
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024'
        }
        
        response = requests.post(dall_e_api_url, headers=headers, json=data)
        
        if response.status_code == 200:
            image_url = response.json()['data'][0]['url']
            return jsonify({"status": "success", "message": "Image created successfully", "image_url": image_url})
        else:
            return jsonify({"error": "Failed to create image. Please try again later."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload image route
@app.route('/user/upload-image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image file provided'}), 400
    file = request.files['image']
    filename = images.save(file)
    return jsonify({'message': 'Image uploaded successfully', 'filename': filename})

## ------ GPT ------ ##

# Route for learning from user interactions
@app.route('/learning/update', methods=['POST'])
@login_required
def update_learning_model():
    user_data = request.get_json()
    # Placeholder for training machine learning model
    return jsonify({'message': 'Model updated with new user data'}), 200


## ------ Dashboard ------ ##

# Route to display posts dashboard
@app.route('/posts/dashboard', methods=['GET'])
@login_required
def posts_dashboard():
    posts = Post.query.all()
    posts_data = [{
        'title': post.title,
        'creation_date': post.creation_date.strftime('%Y-%m-%d'),
        'source_feed': post.source_feed,
        'status': post.status
    } for post in posts]
    return render_template('posts_dashboard.html', posts=posts_data)

    # Route to display scheduled posts
@app.route('/posts/scheduled', methods=['GET'])
@login_required
def show_scheduled_posts():
    scheduled_posts = Post.query.filter_by(status='scheduled').limit(9).all()
    posts_data = [{'title': post.title, 'scheduled_date': post.scheduled_date.strftime('%Y-%m-%d')} for post in scheduled_posts]
    return jsonify({'scheduled_posts': posts_data}), 200

# Route to display dashboard metrics
@app.route('/dashboard/metrics', methods=['GET'])
@login_required
def dashboard_metrics():
    total_posts = Post.query.count()
    pending_approvals = Post.query.filter_by(status='pending').count()
    scheduled_posts = Post.query.filter_by(status='scheduled').count()
    return jsonify({
        'total_posts': total_posts,
        'pending_approvals': pending_approvals,
        'scheduled_posts': scheduled_posts
    })

# Ensure the scheduler starts with the app
scheduler.start()

# WebSocket event for broadcasting updates
@socketio.on('fetch_updates')
def handle_updates(data):
    # Simulated function to fetch new updates
    updates = fetch_new_updates()
    emit('update_response', {'data': updates}, broadcast=True)

def fetch_new_updates():
    # Placeholder function to simulate fetching new data
    return {'new_posts': 5, 'new_comments': 13}

@socketio.on('new_post_approval')
def handle_new_post_approval(post_id):
    socketio.emit('new_post_approval', post_id)

if __name__ == '__main__':
    socketio.run(app)
    
@app.route('/engagement/metrics', methods=['GET'])
@login_required
def get_engagement_metrics():
    top_posts = Post.query.order_by(desc(Post.engagement_score)).limit(10).all()
    metrics = [{'post_id': post.id, 'title': post.title, 'engagement_score': post.engagement_score} for post in top_posts]
    return jsonify(metrics)