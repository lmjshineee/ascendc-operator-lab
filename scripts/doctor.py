"""Read-only environment inventory; never claims NPU validation."""
import json
import platform
import shutil
import sys

ok = sys.version_info >= (3, 11)
print(json.dumps({
    'python': platform.python_version(), 'local_python_supported': ok,
    'system': platform.system(), 'architecture': platform.machine(),
    'git': shutil.which('git'), 'cxx': shutil.which('c++'),
    'npu_smi': shutil.which('npu-smi'),
    'npu_validation': 'not_performed',
    'note': 'Executable discovery is not a device health or CANN compatibility check.'
}, ensure_ascii=False, indent=2))
sys.exit(0 if ok else 1)
