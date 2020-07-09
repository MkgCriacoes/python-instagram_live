import instagram
from flask import request, redirect, render_template
import xmltodict

class Midia:
    def __init__(self, app, stream):
        self.__stream = stream
        self.rotas(app)
    
    def rotas(self, app):
        @app.route("/midia/info")
        def __info():
            stream = self.__stream.value

            #Recebendo informações dos videos e audios e a url principal
            videoInfo = instagram.Midia.info(stream.id)

            url = videoInfo[:videoInfo.index("\n")]
            videoInfo = videoInfo.replace(url + "\n", "")

            url = url[:url.rindex("/")]
            url = url[:url.rindex("/")+1]
            url = url.replace("https://instagram.fnat1-1.fna.fbcdn.net/hvideo-", "")
            videoInfo = videoInfo.replace("../", url)

            videoInfo = xmltodict.parse(videoInfo)

            root = videoInfo["MPD"]["Period"]["AdaptationSet"]
            v = root[0]["Representation"]
            a = root[1]["Representation"]

            v_type = v["@mimeType"]
            a_type = a["@mimeType"]

            v = v["SegmentTemplate"]
            a = a["SegmentTemplate"]

            v_url = v["@media"].replace("../", "")
            a_url = a["@media"].replace("../", "")

            v = v["SegmentTimeline"]["S"]
            a = a["SegmentTimeline"]["S"]

            videos = [{
                "duration": 0,
                "url": v_url.replace("$Time$", "init"),
                "mime_type": v_type
            }]

            audios = [{
                "duration": 0,
                "url": a_url.replace("$Time$", "init"),
                "mime_type": v_type
            }]

            for _v in v:
                videos.append({
                    "duration": _v["@d"],
                    "url": v_url.replace("$Time$", _v["@t"]),
                    "mime_type": v_type
                })

            for _a in a:
                audios.append({
                    "duration": _a["@d"],
                    "url": a_url.replace("$Time$", _a["@t"]),
                    "mime_type": v_type
                })

            media = {
                "videos": videos,
                "audios": audios
            }

            return media