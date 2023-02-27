import consulate
from flask import Flask

app = Flask('app')


@app.route('/toto')
def root():
    return '<h1>Hello, Server! tasks Service</h1>'


@app.route('/')
def run():
    return 'ok'

tags = [
    'traefik.enable=true',
    'traefik.http.routers.approuter.rule=PathPrefix(`/task`)',
    'traefik.http.routers.approuter.entrypoints=web',
    'traefik.http.routers.approuter.service=task-service',
    'traefik.http.services.task-service.loadbalancer.server.port=8000',
    'traefik.http.services.task-service.loadbalancer.server.scheme=http'
]

consul = consulate.Consul()
print(consul.catalog.services())
consul.agent.service.register('task-service', port=8000, tags=tags, interval='2s', httpcheck='http://host.docker.internal:8000')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)