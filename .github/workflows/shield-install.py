import json,subprocess,time
from pathlib import Path
out=Path('verification');out.mkdir(exist_ok=True);checks=[]
def adb(*args):
    result=subprocess.run(['adb',*args],capture_output=True,text=True,timeout=120)
    text=result.stdout+result.stderr
    with (out/'install-log.txt').open('a') as log:log.write('adb '+' '.join(args)+'\n'+text+'\n')
    print(text,flush=True)
    if result.returncode:raise RuntimeError(text)
    return text
try:
    assert 'Success' in adb('install','apks/Glitch-Reflections-TV-2.0.1.apk')
    checks.append('Published TV 2.0.1 installs on a fresh Android TV 11 device')
    adb('shell','am','start','-W','-n','dev.glitchreflections.tv/.MainActivity')
    time.sleep(2)
    (out/'fresh-install.png').write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p']))
    adb('shell','am','force-stop','dev.glitchreflections.tv')
    adb('uninstall','dev.glitchreflections.tv')
    assert 'Success' in adb('install','apks/Glitch-Reflections-TV.apk')
    checks.append('Published TV 2.0.0 installs on Android TV 11')
    assert 'Success' in adb('install','-r','apks/Glitch-Reflections-TV-2.0.1.apk')
    checks.append('Published TV 2.0.1 updates TV 2.0.0 without uninstalling it')
    adb('shell','am','start','-W','-n','dev.glitchreflections.tv/.MainActivity')
    time.sleep(2)
    (out/'updated-install.png').write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p']))
finally:
    (out/'report.json').write_text(json.dumps({'passed':checks},indent=2))
    (out/'logcat.txt').write_text(subprocess.check_output(['adb','logcat','-d','-t','2500'],text=True))
