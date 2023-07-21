def user_listing_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{0}/listings/{1}'.format(instance.seller.user.id, filename)