from django.contrib.auth.decorators import user_passes_test


def allowed_groups(group_names):

    def check(user):

        if user.is_superuser:
            return True

        if user.groups.exists():

            return user.groups.first().name in group_names

        return False

    return user_passes_test(check)