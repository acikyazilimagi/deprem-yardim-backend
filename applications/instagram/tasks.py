from instagram.helpers import bulk_ask_to_zekai, extract_hashtags
from trquake.celery import app
import logging
from django.conf import settings
from instagrapi import Client
from instagrapi.exceptions import ClientError, LoginRequired, BadPassword, ChallengeRequired

from instagram.models import Hashtag, InstagramPost, InstagramSession

logger = logging.getLogger(__name__)

query_words = [
    "1.kat",
    "2.kat",
    "3.kat",
    "4.kat",
    "5.kat",
    "6.kat",
    "7.kat",
    "8.kat",
    "9.kat",
    "10.kat",
    "11.kat",
    "birincikat",
    "ikincikat",
    "üçüncükat",
    "dördüncükat",
    "beşincikat",
    "altıncıkat",
    "yedincikat",
    "sekizincikat",
    "dokuzuncukat",
    "onuncukat",
    "onbirincikat",
    "bina",
    "apartman",
    "apt",
    "mahalle",
    "mahallesi",
    "bulvar",
    "sokak",
    "bulvarı",
    "göçük altında",
    "daire",
    "afad",
    "sk",
    "no:",
]


@app.task
def collect_instagram_posts():
    client = Client()
    session = InstagramSession.objects.filter(is_valid=True).first()
    using_previous_session = False
    if session:
        # https://github.com/adw0rd/instagrapi/blob/5e8f51687e78566e8ddb14ab6e28592ffb81de3e/instagrapi/mixins/auth.py#L535
        client.set_settings(session.settings)
        using_previous_session = True
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
    try:
        for hashtag in Hashtag.objects.all():
            data = []
            medias = client.hashtag_medias_recent(
                hashtag.name, amount=settings.INSTAGRAM_RECENT_POSTS_PER_HASHTAG
            )
            for media in medias:
                if InstagramPost.objects.filter(post_id=media.pk).exists():
                    continue
                has_query_word = False
                caption_text = media.caption_text
                for qw in query_words:
                    if qw in caption_text.lower():
                        has_query_word = True
                        break
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
            bulk_ask_to_zekai(post_data=created_posts)
    except LoginRequired:
        logger.error("Login required error getting data form instagram")
        if using_previous_session:
            session.is_valid = False
            session.save()
    except ClientError as e:
        logger.error(f"Exception raised when getting data form instagram: {e}")
