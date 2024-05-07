# api.py
from flask import Blueprint, send_from_directory, redirect, url_for
from flask_restx import Api, Resource, fields
from models import User, Post, db

api_blueprint = Blueprint('api', __name__, static_folder='static')
api = Api(api_blueprint, version='1.0', title='Oases API', description='Manage content')

@api.route('/favicon.ico', endpoint='api_favicon')
class Favicon(Resource):
    def get(self):
        return send_from_directory(api.app.static_folder, 'favicon.ico')

@api.route('/', endpoint='api_home_redirect')
class Root(Resource):
    def get(self):
        return redirect(url_for(api.endpoint('doc')))

ns = api.namespace('posts', description='Post operations')

post_model = api.model('Post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a post'),
    'content': fields.String(required=True, description='Post content')
})

@ns.route('/', endpoint='posts_list')
class PostList(Resource):
    @ns.doc('list_posts')
    @ns.marshal_list_with(post_model)
    def get(self):
        return Post.query.all()

@ns.route('/<int:id>', endpoint='single_post')
@ns.response(404, 'Post not found')
@ns.param('id', 'The identifier of the post')
class PostResource(Resource):
    @ns.doc('get_post')
    @ns.marshal_with(post_model)
    def get(self, id):
        return Post.query.filter_by(id=id).first_or_404()
