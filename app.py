from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Proxy Metro Granada - Funcionando correctamente ✅'

@app.route('/metro')
def metro():
    try:
        url = "https://metropolitanogranada.es/horariosreal"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Referer': 'https://metropolitanogranada.es/',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return Response(response.text, 
                       mimetype='text/html',
                       headers={
                           'Access-Control-Allow-Origin': '*',
                           'Access-Control-Allow-Methods': 'GET',
                           'Access-Control-Allow-Headers': 'Content-Type'
                       })
    
    except requests.RequestException as e:
        return Response(f'Error obteniendo datos: {str(e)}', status=500)
    except Exception as e:
        return Response(f'Error interno: {str(e)}', status=500)

@app.route('/metro', methods=['OPTIONS'])
def metro_options():
    return Response('', headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)