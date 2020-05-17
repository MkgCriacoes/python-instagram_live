function addComentarioDOM(c_id, c_texto, u_id, u_nome, u_img){
    var comentario = document.createElement("div");
        comentario.id = c_id;
        
    var autor = document.createElement("a");
    autor.innerHTML = "<img src=\"" + u_img + "\" />" + "<span class=\"userId\">@" + u_nome + "</span>";
    
    if(u_id != "" && u_nome != ""){
        autor.id = u_id;
        autor.href = "//instagram.com/" + u_nome;
    }else autor.innerHTML = autor.innerHTML.replace("@", "Sistema");

    var mensagem = document.createElement("p");
    mensagem.innerHTML = c_texto;

    console.log("Novo comentario de " + u_nome + ": " + c_texto);

    comentario.appendChild(autor);
    comentario.appendChild(mensagem);
    div_comentarios.appendChild(comentario);
    
    div_comentarios.scrollTo(0, div_comentarios.scrollHeight);
}

function getComentarios(){
    $.ajax({
        type: "get",
        url: "comentarios",
        data: "lastComent=" + lastComent,
        dataType: "json",
        success: function(data){
            for (var a=0; a < data.length; a+=1){
                var c_id = data[a].id,
                    c_dt_envio = data[a].dt_envio,
                    c_texto = data[a].texto;

                var u = data[a].usuario,
                    u_id = u.id,
                    u_nome = u.nome,
                    u_img = u.img;

                lastComent = c_dt_envio;

                addComentarioDOM(c_id, c_texto, u_id, u_nome, u_img);
            }

            setTimeout(getComentarios, 800);
        },
        error: function(xhr, status, e){
            console.log(e);
            setTimeout(getComentarios, 500);
        }
    });
}

function comentar(){
    $.ajax({
        type: "post",
        url: "comentarios/enviar",
        data: "comentario=" + inpt_comentario.value,
        dataType: "json"
    });

    inpt_comentario.value = "";
}