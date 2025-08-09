from flask import Flask, Response
import requests
import urllib3

# Desactivar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Proxy Metro Granada - Funcionando correctamente ✅'

@app.route('/metro')
def metro():
    try:
        # Lista de URLs a probar
        urls_to_try = [
            "https://metropolitanogranada.es/MGhorariosreal.asp",
            "https://metropolitanogranada.es/horariosreal"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Referer': 'https://metropolitanogranada.es/',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        last_error = None
        
        for url in urls_to_try:
            try:
                print(f"🔍 Probando URL: {url}")
                
                response = requests.get(
                    url, 
                    headers=headers, 
                    timeout=15,
                    verify=False,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                content = response.text
                print(f"✅ Respuesta obtenida de {url}, longitud: {len(content)}")
                
                # Verificar si la respuesta contiene datos útiles
                if (len(content) > 100 and 
                    ('estación' in content.lower() or 
                     'ferrocarril' in content.lower() or
                     'HRdato' in content or
                     'tabla' in content.lower())):
                    
                    print(f"🎯 Datos encontrados en: {url}")
                    
                    return Response(content, 
                                   mimetype='text/html',
                                   headers={
                                       'Access-Control-Allow-Origin': '*',
                                       'Access-Control-Allow-Methods': 'GET',
                                       'Access-Control-Allow-Headers': 'Content-Type',
                                       'X-Data-Source': url
                                   })
                else:
                    print(f"⚠️ {url} no contiene datos útiles: {content[:200]}...")
                    
            except requests.RequestException as e:
                print(f"❌ Error en {url}: {str(e)}")
                last_error = e
                continue
        
        # Si ninguna URL funcionó
        return Response(f'No se pudieron obtener datos de ninguna URL. Último error: {str(last_error)}', 
                       status=503)
    
    except Exception as e:
        return Response(f'Error interno: {str(e)}', status=500)

@app.route('/metro', methods=['OPTIONS'])
def metro_options():
    return Response('', headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    })

# Endpoint de debug para ver qué devuelve cada URL
@app.route('/debug')
def debug():
    try:
        url = "https://metropolitanogranada.es/MGhorariosreal.asp"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        
        return Response(f'''
        <h2>Debug Info</h2>
        <p><strong>Status:</strong> {response.status_code}</p>
        <p><strong>Content Length:</strong> {len(response.text)}</p>
        <p><strong>Content Type:</strong> {response.headers.get('content-type', 'Unknown')}</p>
        <hr>
        <h3>Raw Content (primeros 1000 caracteres):</h3>
        <pre>{response.text[:1000]}</pre>
        ''', mimetype='text/html')
        
    except Exception as e:
        return f'Debug Error: {str(e)}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

