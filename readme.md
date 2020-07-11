## Script em Python para criar e gerenciar lives no Instagram, através do PC
### IDE: VsCode
### Python: 3.8.1; Windows 10 (64 Bits)
### Bibliotecas Usadas: Flask e Requests

O script cria um servidor local na porta 80, no qual torna possivel fazer todas as operações através do navegador.

### Como Usar
Baixe o python (qualquer versão deve funcionar, porém se for usar a versão 2 talvez tenha que alterar algumas coisas).
E execute este comando no cmd ou terminal, para baixar as dependencias necessárias.
```bash
python -m pip install -r requeriments.txt
```
Agora basta iniciar a aplicação através do comando
```bash
python main.py
```
Abra o navegador de sua preferencia (Chrome, Edge, Firefox, Opera, etc), e acesse o endereço [localhost](http://localhost/)
Para encerrar o servidor basta aperta *"ctrl" + "c"* no cmd ou terminal.

### Funcionalidades
- Fazer Login numa interface agradavel
- Gerar chave do Stream, para usar em Softwares de Codec (OBS, StreamLabs OBS, VMix, etc)
- Ver quantas pessoas estão assistindo
- Notificação de que alguma pessoa entrou
- Ver os comentários em tempo real
- Comentar
- Ocultar/Exibir comentários
- Exibir retorno do vídeo
- Exibindo tempo restante para o limite de 1 hora no Instagram

### Script Baseado Nestes Repositórios
- [Instagram-PHP-API](https://github.com/cosenary/Instagram-PHP-API)
- [instagram_private_api](https://github.com/ping/instagram_private_api/tree/master/instagram_private_api)