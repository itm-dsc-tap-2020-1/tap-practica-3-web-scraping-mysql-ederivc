from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import mysql.connector as mysql

def save(pagina: str, cursor: mysql.cursor.MySQLCursor):
    request = Request(
        pagina,
        headers={
            "User-Agent": "FIXME"
        },
    )
    print(f"Checking: {pagina}")
    try:
        html = urlopen(request, timeout=2)
        raw = html.read()
    except Exception:
        return
    soup = BeautifulSoup(raw, "html.parser")
    lista_enlaces = soup.find_all("a")
    for enlace in lista_enlaces:
        try:
            url: str = enlace["href"]
        except KeyError:
            continue
        if not url.startswith("http"):
            continue
        try:
            operacion.execute(f'INSERT INTO paginas VALUES ("{url}", false)')
        except mysql.errors.IntegrityError:
            continue


conexion = mysql.connect(host="localhost", user="root", passwd="", db="paginas")
operacion = conexion.cursor(buffered=True)

website = input("Ingrese una pagina web: ")
save(website, operacion)

while True:
    operacion.execute("SELECT * FROM paginas WHERE status=FALSE")
    pagina = operacion.fetchone()
    if not pagina:
        break
    url = pagina[0]
    try:
        save(url, operacion)
    except Exception as e:
        operacion.execute(f'UPDATE paginas SET status=TRUE WHERE url="{url}"')
        continue
    operacion.execute(f'UPDATE paginas SET status=TRUE WHERE url="{url}"')
    operacion.execute("SELECT * FROM paginas")
    rows = operacion.fetchall()
    print(f"Entradas: {len(rows)}")
    conexion.commit()

conexion.close()