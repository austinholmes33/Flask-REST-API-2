from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __init__(self, name, views, likes):
        self.name = name
        self.views = views
        self.likes = likes

    def __repr__(self):
        return f"Video(name={self.name}, views={self.views}, likes={self.likes})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video")
video_put_args.add_argument("views", type=int, help="Views of the video")
video_put_args.add_argument("likes", type=int, help="Likes of the video")

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

# def abort_if_video_id_does_not_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="Video id not valid")

# def abort_if_video_exists(video_id):
#     if video_id in videos:
#         abort(409, message="Video already exists with that id")

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that id")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id taken")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video does not exist")
        if args["name"]:
            result.name = args['name']
        if args["views"]:
            result.views = args['views']
        if args["likes"]:
            result.likes = args['likes']

        db.session.commit()
        return result

    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        del(result)
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")
# class HelloWorld(Resource):
#     def get(self, name):
#         # serializable information - dictionary(json format)
#         return names[name]


# api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)