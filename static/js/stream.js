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

function atualizarTRestante(){
    setInterval(function(){
        var now = new Date().getTime();
        var dif = startTime - now;
        dif = new Date(dif);
        dif.setHours(0);

        var options = {
            "hour": "numeric",
            "minute": "numeric",
            "second": "numeric"
        };
        document.getElementById("tRestante").innerText = dif.toLocaleString("pt-BR", options);
    }, 1000);
}

