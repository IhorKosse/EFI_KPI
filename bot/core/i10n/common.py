import settings


UA = "ua"
EN = "en"
IT = "it"


def gen_response(en_func, ua_func, it_func, *args, **kwargs):
    if settings.LOCALIZATION == "en":
        return en_func(*args, **kwargs)

    elif settings.LOCALIZATION == "ua":
        return ua_func(*args, **kwargs)

    elif settings.LOCALIZATION == "it":
        return it_func(*args, **kwargs)

    else:
        raise ValueError("Unknown localization set in settings")
