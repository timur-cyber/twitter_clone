"""Init migration

Revision ID: 8604d393e55a
Revises: 
Create Date: 2023-03-22 22:37:23.157641

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "8604d393e55a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "media",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("link", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_media_id"), "media", ["id"], unique=False)
    op.create_index(op.f("ix_media_link"), "media", ["link"], unique=False)
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("api_key"),
    )
    op.create_table(
        "follow",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("following_user_id", sa.Integer(), nullable=True),
        sa.Column("followed_user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["followed_user_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["following_user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_follow_followed_user_id"), "follow", ["followed_user_id"], unique=False
    )
    op.create_index(
        op.f("ix_follow_following_user_id"),
        "follow",
        ["following_user_id"],
        unique=False,
    )
    op.create_index(op.f("ix_follow_id"), "follow", ["id"], unique=False)
    op.create_table(
        "tweet",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("text", sa.String(), nullable=True),
        sa.Column("data", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("datetime", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_tweet_id"), "tweet", ["id"], unique=False)
    op.create_index(op.f("ix_tweet_text"), "tweet", ["text"], unique=False)
    op.create_index(op.f("ix_tweet_user_id"), "tweet", ["user_id"], unique=False)
    op.create_table(
        "like",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("tweet_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["tweet_id"], ["tweet.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_like_id"), "like", ["id"], unique=False)
    op.create_index(op.f("ix_like_user_id"), "like", ["user_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_like_user_id"), table_name="like")
    op.drop_index(op.f("ix_like_id"), table_name="like")
    op.drop_table("like")
    op.drop_index(op.f("ix_tweet_user_id"), table_name="tweet")
    op.drop_index(op.f("ix_tweet_text"), table_name="tweet")
    op.drop_index(op.f("ix_tweet_id"), table_name="tweet")
    op.drop_table("tweet")
    op.drop_index(op.f("ix_follow_id"), table_name="follow")
    op.drop_index(op.f("ix_follow_following_user_id"), table_name="follow")
    op.drop_index(op.f("ix_follow_followed_user_id"), table_name="follow")
    op.drop_table("follow")
    op.drop_table("user")
    op.drop_index(op.f("ix_media_link"), table_name="media")
    op.drop_index(op.f("ix_media_id"), table_name="media")
    op.drop_table("media")
    # ### end Alembic commands ###
