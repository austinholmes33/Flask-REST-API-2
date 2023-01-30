from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

names = {"tim": {"age": 19, "gender": "man"},
        "bill": {"age": 70, "gender": "man"}}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video")
video_put_args.add_argument("views", type=int, help="Views of the video")
video_put_args.add_argument("likes", type=int, help="Likes of the video")

videos = {}

def about_if_video_id_does_not_exist(video_id):
    if video_id not in videos:
        abort("Video id not valid")

class Video(Resource):
    def get(self, video_id):
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id]

api.add_resource(Video, "/video/<int:video_id>")
# class HelloWorld(Resource):
#     def get(self, name):
#         # serializable information - dictionary(json format)
#         return names[name]


# api.add_resource(HelloWorld, "/helloworld/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)