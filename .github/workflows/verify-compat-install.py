"""Compare the known-working original, published TV APK, and compatibility build."""
import json, subprocess
from pathlib import Path
out=Path('tv/verification');out.mkdir(exist_ok=True)
checks=[]
def install(path):
    result=subprocess.run(['adb','install',str(path)],capture_output=True,text=True,timeout=180)
    text=result.stdout+result.stderr
    with (out/'compatibility-install-log.txt').open('a') as log:log.write(str(path)+'\n'+text+'\n')
    print(text,flush=True)
    return result.returncode,text
try:
    code,text=install('tv/original-artwork.apk')
    assert code==0 and 'Success' in text,text
    checks.append('Original APK supplied through Drive installs successfully')
    sdk=int(subprocess.check_output(['adb','shell','getprop','ro.build.version.sdk'],text=True).strip())
    if sdk<28:
        code,text=install('apks/Glitch-Reflections-TV-2.0.1.apk')
        assert code!=0 and 'INSTALL_FAILED_OLDER_SDK' in text,text
        checks.append('Published TV 2.0.1 fails with INSTALL_FAILED_OLDER_SDK on Android '+str(sdk))
    code,text=install('tv/build/test.apk')
    assert code==0 and 'Success' in text,text
    checks.append('TV 2.0.2 compatibility candidate installs alongside original app')
finally:
    (out/'compatibility-install-report.json').write_text(json.dumps({'checks':checks},indent=2))
