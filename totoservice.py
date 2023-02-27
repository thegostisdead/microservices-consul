import consulate
from flask import Flask

app = Flask('app')


@app.route('/toto')
def root():
    return '<h1>Hello, Server! TOTO Service</h1>'


@app.route('/')
def run():
    return 'ok'

tags = [
    'traefik.enable=true',
    'traefik.http.routers.approuter.rule=PathPrefix(`/toto`)',
    'traefik.http.routers.approuter.entrypoints=web',
    'traefik.http.routers.approuter.service=toto-service',
    'traefik.http.services.toto-service.loadbalancer.server.port=9000',
    'traefik.http.services.toto-service.loadbalancer.server.scheme=http'
]

consul = consulate.Consul()
print(consul.catalog.services())
consul.agent.service.register('toto-service', port=9000, tags=tags, interval='2s', httpcheck='http://host.docker.internal:9000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)