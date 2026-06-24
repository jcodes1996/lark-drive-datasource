import os
import uuid
from pathlib import Path

os.chdir(Path(__file__).parent)

from dify_plugin.core.plugin_registration import PluginRegistration
from dify_plugin.config.config import DifyPluginEnv

config = DifyPluginEnv()
reg = PluginRegistration(config)

print('=== Checking plugin classes ===')
provider_cls = reg.get_datasource_provider_cls('lark_drive')
print(f'Provider class: {provider_cls}')

datasource_cls = reg.get_online_drive_datasource_cls('lark_drive', 'lark_drive')
print(f'Datasource class: {datasource_cls}')

# Try to instantiate provider
print()
print('=== Instantiating provider ===')
provider = provider_cls()
print(f'Provider instance: {provider}')

print()
print('=== Instantiating datasource ===')
from dify_plugin.core.runtime import DatasourceRuntime
from dify_plugin.core.entities.session import Session

session = Session(
    session_id=uuid.uuid4().hex,
    executor=None,
    reader=None,
    writer=None,
    install_method='local',
    dify_plugin_daemon_url='',
    conversation_id=None,
    message_id=None,
    app_id=None,
    endpoint_id=None,
    context={},
    max_invocation_timeout=30,
)

runtime = DatasourceRuntime(config=config, session=session)
ds = datasource_cls(runtime=runtime, session=session)
print(f'Datasource instance: {ds}')

# Test browse_files method signature
print()
print('=== Checking method signatures ===')
import inspect
print(f'_browse_files: {inspect.signature(ds._browse_files)}')
print(f'_download_file: {inspect.signature(ds._download_file)}')

print()
print('All OK!')
