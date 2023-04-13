from flasgger import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    name = fields.Str(required=True)


class TweetSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    user_id = fields.Int(required=True)
    text = fields.Str(required=True)
    media = fields.String(required=False)


class MediaSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    link = fields.Str(required=True)


class LikeSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    user_id = fields.Int(required=True)
    tweet_id = fields.Int(required=True)


class FollowSchema(Schema):
    id = fields.Int(dump_only=True, required=True)
    following_user_id = fields.Int(required=True)
    followed_user_id = fields.Int(required=True)
