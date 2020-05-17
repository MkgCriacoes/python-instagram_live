function getInfo(){
    $.ajax({
        type: "get",
        url: "stream/info",
        dataType: "json",
        success: function(data){
            console.log(data);

            var viewCount = data.viewer_count;
            var status = data.broadcast_status;

            div_asistindo.innerHTML = "AO VIVO<span>" + viewCount + "</span>";

            if (status == "stoped"){
                location.href = "stream/encerrar";
                return;
            }

            setTimeout(getInfo, 2000);
        },
        error: function(xhr, status, e){
            console.log(e);
            setTimeout(getInfo, 1500);
        }
    });
}