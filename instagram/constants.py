import uuid

class Constants:
    """Baseado no código da api privada do instagram
       https://github.com/ping/instagram_private_api/tree/master/instagram_private_api
    """

    APP_VERSION = '76.0.0.15.395'

    ANDROID_VERSION = 24
    ANDROID_RELEASE = '7.0'
    PHONE_MANUFACTURER = 'motorola'
    PHONE_DEVICE = 'Moto C Plus'
    PHONE_MODEL = 'panell_23_dl'
    PHONE_DPI = '240dpi'
    PHONE_RESOLUTION = '720x1280'
    PHONE_CHIPSET = 'mt6737'
    VERSION_CODE = '138226743'

    USER_AGENT_FORMAT = \
        "Mozilla/5.0 (Linux; Android {android_release}; {device}; wv) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 " \
        "Chrome/80.0.3987.99 Mobile Safari/537.36 " \
        "Instagram {app_version} Android ({android_version:d}/{android_release}; " \
        "{dpi}; {resolution}; {brand}; {device}; {model}; {chipset}; en_US; {version_code})"

    USER_AGENT = USER_AGENT_FORMAT.format(**{
        'app_version': APP_VERSION,
        'android_version': ANDROID_VERSION,
        'android_release': ANDROID_RELEASE,
        'brand': PHONE_MANUFACTURER,
        'device': PHONE_DEVICE,
        'model': PHONE_MODEL,
        'dpi': PHONE_DPI,
        'resolution': PHONE_RESOLUTION,
        'chipset': PHONE_CHIPSET,
        'version_code': VERSION_CODE})

    DEVICE = uuid.uuid1()
    ANDROID_DEVICE = "android:%s" % DEVICE