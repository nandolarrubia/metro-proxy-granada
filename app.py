from flask import Flask, Response, request
import requests
import urllib3
from datetime import datetime

# Desactivar warnings SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Proxy Metro Granada - Funcionando correctamente ✅'

@app.route('/metro')
def metro():
    try:
        # Probar múltiples URLs y métodos
        urls_to_try = [
            "https://metropolitanogranada.es/MGhorariosreal.asp",
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Referer': 'https://metropolitanogranada.es/',
            'Connection': 'keep-alive'
        }
        
        for url in urls_to_try:
            try:
                response = requests.get(url, headers=headers, verify=False, timeout=15)
                
                if response.status_code == 200 and len(response.text) > 50:
                    content = response.text
                    
                    # Verificar si contiene datos útiles
                    if ('no hay datos' not in content.lower() and 
                        ('estación' in content.lower() or 'HRdato' in content)):
                        
                        return Response(content, 
                                       mimetype='text/html',
                                       headers={
                                           'Access-Control-Allow-Origin': '*',
                                           'Access-Control-Allow-Methods': 'GET',
                                           'Access-Control-Allow-Headers': 'Content-Type',
                                           'X-Data-Source': url
                                       })
                        
            except:
                continue
        
        # Si no hay datos reales, devolver mensaje informativo
        now = datetime.now().strftime("%H:%M")
        return Response(f'''
        <div style="text-align: center; padding: 20px;">
            <h3>No hay datos disponibles en este momento</h3>
            <p>Hora actual: {now}</p>
            <p>El servicio del metro puede estar:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>🌙 Cerrado (fuera del horario de servicio)</li>
                <li>🔧 En mantenimiento</li>
                <li>⏸️ Temporalmente pausado</li>
            </ul>
            <p><em>La aplicación usará datos simulados mientras tanto.</em></p>
        </div>
        ''', 
        mimetype='text/html',
        headers={'Access-Control-Allow-Origin': '*'})
    
    except Exception as e:
        return Response(f'Error interno: {str(e)}', status=500)

@app.route('/debug')
def debug():
    try:
        now = datetime.now()
        info = f'''
        <h2>Debug Metro Granada</h2>
        <p><strong>Hora actual:</strong> {now.strftime("%Y-%m-%d %H:%M:%S")}</p>
        <hr>
        '''
        
        urls_to_test = [
            "https://metropolitanogranada.es/MGhorariosreal.asp",
        ]
        
        for url in urls_to_test:
            try:
                response = requests.get(url, verify=False, timeout=10)
                info += f'''
                <h3>{url}</h3>
                <p><strong>Status:</strong> {response.status_code}</p>
                <p><strong>Content Length:</strong> {len(response.text)}</p>
                <p><strong>Content Type:</strong> {response.headers.get('content-type', 'Unknown')}</p>
                <details>
                    <summary>Ver contenido</summary>
                    <pre style="background: #f5f5f5; padding: 10px; overflow: auto;">{response.text[:2000]}</pre>
                </details>
                <hr>
                '''
            except Exception as e:
                info += f'<p><strong>{url}:</strong> Error - {str(e)}</p><hr>'
        
        return Response(info, mimetype='text/html')
        
    except Exception as e:
        return f'Debug Error: {str(e)}'

@app.route('/metro', methods=['OPTIONS'])
def metro_options():
    return Response('', headers={
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

