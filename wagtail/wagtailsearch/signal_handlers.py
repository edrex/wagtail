from django.db.models.signals import post_save, post_delete

from wagtail.wagtailsearch.index import Indexed, get_indexed_models
from wagtail.wagtailsearch.backends import get_search_backends


def post_save_signal_handler(instance, **kwargs):
    if instance not in type(instance).get_indexed_objects():
        return


    for backend in get_search_backends():
        backend.add(instance)


def post_delete_signal_handler(instance, **kwargs):
    if instance not in type(instance).get_indexed_objects():
        return

    for backend in get_search_backends():
        backend.delete(instance)


def register_signal_handlers():
    # Loop through list and register signal handlers for each one
    for model in get_indexed_models():
        post_save.connect(post_save_signal_handler, sender=model)
        post_delete.connect(post_delete_signal_handler, sender=model)
