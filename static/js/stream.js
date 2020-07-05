function getInfo(){
    $.ajax({
        type: "get",
        url: "stream/info",
        dataType: "json",
        success: function(data){
            var viewCount = data.viewer_count;
            var status = data.broadcast_status;

            if (status == "interrupted"){
                div_asistindo.innerHTML = "PAUSADO<span>.</span>";
            }else if (status == "stopped"){
                location.href = "stream/encerrar";
                return;
            }else{
                div_asistindo.innerHTML = "AO VIVO<span>" + viewCount + "</span>";
            }

            setTimeout(getInfo, 2000);
        },
        error: function(xhr, status, e){
            console.log(e);
            setTimeout(getInfo, 1500);
        }
    });
}