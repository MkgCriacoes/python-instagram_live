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

    USER_AGENT = \
        "Mozilla/5.0 (Linux; Android %s; %s; wv) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 " \
        "Chrome/%s Mobile Safari/537.36 " \
        "Instagram %s Android (%s/%s; " \
        "%s; %s; %s; %s; %s; %s; en_US; %s)" % (
            ANDROID_RELEASE,
            PHONE_DEVICE,
            CHROME_VERSION,
            APP_VERSION,
            ANDROID_VERSION,
            ANDROID_RELEASE,
            PHONE_DPI,
            PHONE_RESOLUTION,
            PHONE_MANUFACTURER,
            PHONE_DEVICE,
            PHONE_MODEL,
            PHONE_CHIPSET,
            VERSION_CODE
        )

    USER_AGENT_DESKTOP = \
        "Mozilla/5.0 (Windows NT %s; Win64; x64) " \
        "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 " \
        "Chrome/%s Safari/537.36" % (
            WIN_VERSION,
            CHROME_VERSION
        )

    DEVICE = uuid.uuid1()
    ANDROID_DEVICE = "android:%s" % DEVICE