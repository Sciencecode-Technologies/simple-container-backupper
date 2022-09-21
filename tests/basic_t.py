from conback.core import ConbackCore


cbk = ConbackCore()

print(cbk.config['General'])
print(cbk.config['General']['id_len'])

print(cbk.list_active_containers())