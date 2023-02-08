from instagram.helpers import (
    bulk_ask_instagram_posts_to_zekai,
    bulk_ask_instagram_comments_to_zekai,
    extract_hashtags,
    contains_query_word,
)
from trquake.celery import app
import logging
from django.conf import settings
from instagrapi import Client
from instagrapi.exceptions import (
    ClientError,
    LoginRequired,
    BadPassword,
    ChallengeRequired,
)

from instagram.models import (
    Hashtag,
    InstagramPost,
    InstagramSession,
    InstagramPostToFollow,
    InstagramComment,
)

logger = logging.getLogger(__name__)


def get_instagram_client():
    client = Client()
    session = InstagramSession.objects.filter(is_valid=True).first()
    if session:
        # https://github.com/adw0rd/instagrapi/blob/5e8f51687e78566e8ddb14ab6e28592ffb81de3e/instagrapi/mixins/auth.py#L535
        client.set_settings(session.settings)
    elif settings.INSTAGRAM_USERNAME and settings.INSTAGRAM_PASSWORD:
        try:
            client.login(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
            logger.info("Successfully logged in, persisting the session data")
            session = InstagramSession.objects.create(
                settings=client.get_settings(), username=settings.INSTAGRAM_USERNAME
            )
        except BadPassword:
            logger.error(
                "Password provided via settings is invalid, attempting to keep without authentication"
            )
        except ClientError as e:
            logger.error(
                f"Error logging in: {e}. Attempting to keep without authentication"
            )
        except ChallengeRequired:
            logger.error(
                "Challenge is required to login, it can be solved using the `create_instagram_session` command, attempting to keep without authentication"
            )
    return client, session


@app.task
def collect_instagram_posts():
    client, session = get_instagram_client()
    try:
        for hashtag in Hashtag.objects.all():
            data = []
            medias = client.hashtag_medias_recent(
                hashtag.name, amount=settings.INSTAGRAM_RECENT_POSTS_PER_HASHTAG
            )
            for media in medias:
                if InstagramPost.objects.filter(post_id=media.pk).exists():
                    continue
                has_query_word = contains_query_word(media.caption_text)
                if has_query_word:
                    post = InstagramPost(
                        user_id=media.user.pk,
                        screen_name=media.user.full_name,
                        name=media.user.username,
                        post_id=media.pk,
                        created_at=media.taken_at,
                        full_text=media.caption_text,
                        hashtags=extract_hashtags(media.caption_text),
                        media=media.thumbnail_url,
                    )
                    # Instagram can also provide some information from the post which might be useful
                    # Accessible through: media.location.address / media.location.lat / media.location.lng
                    data.append(post)

            created_posts = InstagramPost.objects.bulk_create(data)
            logger.info(
                f"{len(created_posts)} created posts for hashtag: {hashtag.name}"
            )
            bulk_ask_instagram_posts_to_zekai(post_data=created_posts)
    except LoginRequired:
        logger.error("Login required error getting data form instagram")
        if session:
            session.is_valid = False
            session.save()
    except ClientError as e:
        logger.error(f"Exception raised when getting data form instagram: {e}")


@app.task
def collect_instagram_comments():
    client, session = get_instagram_client()
    try:
        for media in InstagramPostToFollow.objects.all():
            media_id = client.media_pk_from_url(media.url)
            # if not InstagramPost.objects.filter(post_id=media_id).exists():
            #     media_info = client.media_info(media_id)

            data = []
            comments = client.media_comments(media_id)
            for comment in comments:
                if InstagramComment.objects.filter(comment_id=comment.pk).exists():
                    continue
                has_query_word = contains_query_word(comment.text)
                if has_query_word:
                    new_comment = InstagramComment(
                        followed_post_id=media.pk,
                        user_id=comment.user.pk,
                        screen_name=comment.user.full_name,
                        name=comment.user.username,
                        post_id=media_id,
                        comment_id=comment.pk,
                        created_at=comment.created_at_utc,
                        full_text=comment.text,
                        is_active=True if comment.status == "Active" else False,
                    )
                    data.append(new_comment)

            created_comments = InstagramComment.objects.bulk_create(data)
            logger.info(f"{len(created_comments)} created posts from post: {media.pk}")
            bulk_ask_instagram_comments_to_zekai(comments_data=created_comments)
    except LoginRequired:
        logger.error("Login required error getting data form instagram")
        if session:
            session.is_valid = False
            session.save()
    except ClientError as e:
        logger.error(f"Exception raised when getting data form instagram: {e}")
