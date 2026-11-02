"""Exercise the exact release APK through the TV package installer's UI.

The temporary provider is only an emulator fixture. It is never distributed
with, or used to re-sign, the release APK.
"""
import hashlib
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

OUT = Path('verification')
OUT.mkdir(exist_ok=True)
WORK = Path('installer-fixture')
WORK.mkdir(exist_ok=True)
FIXTURE = 'dev.glitchreflections.installerfixture'
TARGET = 'dev.glitchreflections.tv'
APK = Path('apks/Glitch-Reflections-TV-2.0.1.apk')
checks = []

def run(*args, **kwargs):
    result = subprocess.run(list(map(str, args)), capture_output=True, timeout=180, **kwargs)
    output = (result.stdout + result.stderr).decode(errors='replace')
    with (OUT / 'installer-ui-log.txt').open('a') as log:
        log.write(' '.join(map(str, args)) + '\n' + output + '\n')
    print(output, flush=True)
    if result.returncode:
        raise RuntimeError(output)
    return output

def adb(*args, **kwargs):
    return run('adb', *args, **kwargs)

def screenshot(name):
    (OUT / (name + '.png')).write_bytes(subprocess.check_output(['adb', 'exec-out', 'screencap', '-p']))

def dump():
    for attempt in range(4):
        adb('shell', 'rm', '-f', '/sdcard/installer-ui.xml')
        adb('shell', 'uiautomator', 'dump', '/sdcard/installer-ui.xml')
        result = subprocess.run(['adb', 'exec-out', 'cat', '/sdcard/installer-ui.xml'], capture_output=True)
        try:
            root = ET.fromstring(result.stdout)
            (OUT / 'installer-ui.xml').write_bytes(result.stdout)
            return root
        except ET.ParseError:
            time.sleep(1)
    raise RuntimeError('Could not read installer screen')

sdk = Path(os.environ.get('ANDROID_HOME', '/usr/local/lib/android/sdk'))
tools = max((sdk / 'build-tools').iterdir(), key=lambda p: tuple(int(x) for x in re.findall(r'\d+', p.name)))
android = sdk / 'platforms/android-30/android.jar'
manifest = '''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="dev.glitchreflections.installerfixture" android:versionCode="1"><uses-sdk android:minSdkVersion="23" android:targetSdkVersion="30"/><uses-permission android:name="android.permission.REQUEST_INSTALL_PACKAGES"/><application android:label="Emulator installer fixture" android:debuggable="true"><activity android:name=".MainActivity" android:exported="true"/><provider android:name=".ApkProvider" android:authorities="dev.glitchreflections.installerfixture.apk" android:exported="false" android:grantUriPermissions="true"/></application></manifest>'''
main = '''package dev.glitchreflections.installerfixture;
import android.app.Activity; import android.os.Bundle; import android.content.Intent; import android.net.Uri;
public class MainActivity extends Activity {
  public void onCreate(Bundle state) {
    super.onCreate(state);
    Intent intent=new Intent(Intent.ACTION_VIEW);
    intent.setDataAndType(Uri.parse("content://dev.glitchreflections.installerfixture.apk/base.apk"),"application/vnd.android.package-archive");
    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
    startActivity(intent);
  }
}'''
provider = '''package dev.glitchreflections.installerfixture;
import android.content.ContentProvider; import android.content.ContentValues; import android.database.Cursor; import android.database.MatrixCursor; import android.net.Uri; import android.os.ParcelFileDescriptor; import java.io.File; import java.io.FileNotFoundException;
public class ApkProvider extends ContentProvider {
  private File file(){return new File(getContext().getFilesDir(),"target.apk");}
  public boolean onCreate(){return true;}
  public String getType(Uri uri){return "application/vnd.android.package-archive";}
  public ParcelFileDescriptor openFile(Uri uri,String mode) throws FileNotFoundException {return ParcelFileDescriptor.open(file(),ParcelFileDescriptor.MODE_READ_ONLY);}
  public Cursor query(Uri uri,String[] projection,String selection,String[] args,String sort){MatrixCursor c=new MatrixCursor(new String[]{"_display_name","_size"}); c.addRow(new Object[]{"Glitch-Reflections-TV-2.0.1.apk",file().length()}); return c;}
  public Uri insert(Uri uri,ContentValues v){throw new UnsupportedOperationException();}
  public int update(Uri uri,ContentValues v,String s,String[] a){throw new UnsupportedOperationException();}
  public int delete(Uri uri,String s,String[] a){throw new UnsupportedOperationException();}
}'''

try:
    assert hashlib.file_digest(APK.open('rb'), 'sha256').hexdigest() == 'c107d79c4ea84b1b4a8193847380634600cc24d6a316ddfadcf0ae4b017b9eb3'
    (WORK / 'AndroidManifest.xml').write_text(manifest)
    (WORK / 'MainActivity.java').write_text(main)
    (WORK / 'ApkProvider.java').write_text(provider)
    (WORK / 'classes').mkdir(exist_ok=True)
    (WORK / 'dex').mkdir(exist_ok=True)
    run(tools / 'aapt2', 'link', '--manifest', WORK / 'AndroidManifest.xml', '-I', android, '-o', WORK / 'fixture-unsigned.apk')
    run('javac', '--release', '8', '-classpath', android, '-d', WORK / 'classes', WORK / 'MainActivity.java', WORK / 'ApkProvider.java')
    run(tools / 'd8', '--lib', android, '--min-api', '23', '--output', WORK / 'dex', *sorted((WORK / 'classes').rglob('*.class')))
    with zipfile.ZipFile(WORK / 'fixture-unsigned.apk', 'a') as archive:
        archive.write(WORK / 'dex/classes.dex', 'classes.dex', compress_type=zipfile.ZIP_DEFLATED)
    run(tools / 'zipalign', '-f', '4', WORK / 'fixture-unsigned.apk', WORK / 'fixture-aligned.apk')
    run('keytool', '-genkeypair', '-keystore', WORK / 'fixture.jks', '-alias', 'emulator-fixture', '-keyalg', 'RSA', '-validity', '2', '-dname', 'CN=Ephemeral emulator fixture only', '-storepass', 'android', '-keypass', 'android')
    run(tools / 'apksigner', 'sign', '--ks', WORK / 'fixture.jks', '--ks-pass', 'pass:android', '--out', WORK / 'fixture.apk', WORK / 'fixture-aligned.apk')
    subprocess.run(['adb', 'uninstall', TARGET], capture_output=True)
    adb('install', WORK / 'fixture.apk')
    adb('shell', 'run-as', FIXTURE, 'mkdir', '-p', 'files')
    with APK.open('rb') as source:
        adb('shell', '-T', 'run-as ' + FIXTURE + " sh -c 'cat > files/target.apk'", stdin=source)
    size = adb('shell', 'run-as', FIXTURE, 'wc', '-c', 'files/target.apk')
    assert str(APK.stat().st_size) in size
    # Grant this throwaway source permission inside the emulator only.
    adb('shell', 'appops', 'set', FIXTURE, 'REQUEST_INSTALL_PACKAGES', 'allow')
    adb('shell', 'am', 'start', '-W', '-n', FIXTURE + '/.MainActivity')
    time.sleep(2)
    screenshot('installer-confirmation')
    root = dump()
    buttons = [node for node in root.iter('node') if node.get('text', '').lower() == 'install']
    if not buttons:
        raise RuntimeError('No Install button on screen: ' + ET.tostring(root).decode())
    bounds = list(map(int, re.findall(r'\d+', buttons[0].get('bounds', ''))))
    adb('shell', 'input', 'tap', str((bounds[0] + bounds[2]) // 2), str((bounds[1] + bounds[3]) // 2))
    for attempt in range(20):
        root = dump()
        texts = ' '.join(node.get('text', '') for node in root.iter('node'))
        print('INSTALLER SCREEN:', texts, flush=True)
        if 'not installed' in texts.lower() or "couldn't be installed" in texts.lower():
            raise RuntimeError('System installer rejected APK: ' + texts)
        if 'app installed' in texts.lower() or 'successfully installed' in texts.lower():
            checks.append('Published TV 2.0.1 installs through the on-screen Android TV 11 installer from a granted content URI')
            break
        time.sleep(1)
    else:
        raise RuntimeError('Installer did not show a completed installation')
    screenshot('installer-success')
    adb('shell', 'am', 'start', '-W', '-n', TARGET + '/.MainActivity')
    time.sleep(2)
    screenshot('installer-launched-app')
finally:
    screenshot('installer-final-screen')
    (OUT / 'installer-ui-report.json').write_text(json.dumps({'passed': checks}, indent=2))
    (OUT / 'installer-logcat.txt').write_text(subprocess.check_output(['adb', 'logcat', '-d', '-t', '3500'], text=True))
