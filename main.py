import instagram
import time

instagram.fazerLogin("USUARIO", "SENHA")
stream = instagram.getStream()

time.sleep(2)
stream.iniciar()

time.sleep(2)
stream.encerrar()