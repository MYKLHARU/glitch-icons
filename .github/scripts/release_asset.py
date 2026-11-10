"""Upload a checksum-verified finished artifact to an existing GitHub release.

APK inputs must be signed with the pack's existing TV key. The private key is
never supplied to this workflow. Existing assets are never overwritten.
"""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,urllib.parse,urllib.request

SIGNER='4082d41cca39077124c717d05fac8af9731c7e7636647bdf853de52c3f238ed1'
PACKAGE='dev.glitchreflections.tv'

def inputs():
    name=os.environ['ASSET_NAME'];expected=os.environ['EXPECTED_SHA256'].lower()
    tag=os.environ['RELEASE_TAG']
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,180}',name):
        raise ValueError('Use a plain asset filename without path separators')
    if not re.fullmatch(r'[a-f0-9]{64}',expected):
        raise ValueError('Expected SHA-256 must contain 64 hexadecimal characters')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]{0,120}',tag):
        raise ValueError('Invalid release tag')
    return name,expected,tag

def sha256(path):
    with path.open('rb') as file:return hashlib.file_digest(file,'sha256').hexdigest()

def verify_apk(path):
    sdk=Path(os.environ.get('ANDROID_HOME',os.environ.get('ANDROID_SDK_ROOT','/usr/local/lib/android/sdk')))
    configured=os.environ.get('BUILD_TOOLS')
    choices=[Path(configured)/'apksigner'] if configured else sorted(sdk.glob('build-tools/*/apksigner'))
    choices=[p for p in choices if p.is_file()]
    if not choices:raise RuntimeError('Android SDK apksigner is unavailable')
    tools=choices[-1].parent
    output=subprocess.check_output([str(tools/'apksigner'),'verify','--print-certs',str(path)],text=True,stderr=subprocess.STDOUT)
    signers=re.findall(r'^Signer #\d+ certificate SHA-256 digest: ([a-f0-9]+)$',output,re.MULTILINE)
    if signers!=[SIGNER]:raise ValueError('APK must use the existing Glitch Reflections TV signing key')
    badging=subprocess.check_output([str(tools/'aapt2'),'dump','badging',str(path)],text=True)
    if not badging.startswith("package: name='"+PACKAGE+"'"):
        raise ValueError('APK package does not match Glitch Reflections TV')
    subprocess.run([str(tools/'zipalign'),'-c','-p','4',str(path)],check=True)

class HttpsRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if urllib.parse.urlsplit(newurl).scheme!='https':
            raise ValueError('Download redirects must remain HTTPS')
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def artifact(name):
    return Path(os.environ.get('RUNNER_TEMP','.'))/'release-upload'/name

def download():
    name,expected,_=inputs();url=os.environ['ASSET_URL']
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Provide a direct HTTPS download URL without login credentials')
    print('::add-mask::'+url,flush=True)
    target=artifact(name);target.parent.mkdir(parents=True,exist_ok=True)
    opener=urllib.request.build_opener(HttpsRedirects())
    request=urllib.request.Request(url,headers={'User-Agent':'Glitch-Reflections-release-upload'})
    try:
        with opener.open(request,timeout=60) as response,target.open('wb') as output:
            count=0
            while chunk:=response.read(1024*1024):
                count+=len(chunk)
                if count>2*1024**3:raise ValueError('Asset exceeds 2 GiB')
                output.write(chunk)
    except Exception:
        target.unlink(missing_ok=True)
        raise RuntimeError('HTTPS artifact download failed; check the URL and expiry') from None
    if not target.stat().st_size or sha256(target)!=expected:
        target.unlink(missing_ok=True);raise ValueError('Downloaded file SHA-256 does not match')
    if name.lower().endswith('.apk'):verify_apk(target)
    print('Verified finished artifact:',name,flush=True)

def gh(*args):
    return subprocess.check_output(['gh',*args],text=True)

def publish():
    name,expected,tag=inputs();target=artifact(name)
    if not target.is_file() or sha256(target)!=expected:
        raise ValueError('A verified local artifact is required before upload')
    repository=os.environ['GITHUB_REPOSITORY']
    endpoint='repos/'+repository+'/releases/tags/'+urllib.parse.quote(tag,safe='')
    release=json.loads(gh('api',endpoint))
    existing=next((a for a in release['assets'] if a['name']==name),None)
    if existing:
        if existing.get('digest')!='sha256:'+expected:
            raise ValueError('This filename already exists with different or unverifiable content; use a new versioned name')
        asset=existing;status='Already published; checksum matches'
    else:
        subprocess.run(['gh','release','upload',tag,str(target),'--repo',repository],check=True)
        release=json.loads(gh('api',endpoint))
        asset=next(a for a in release['assets'] if a['name']==name)
        if asset.get('digest')!='sha256:'+expected or asset['size']!=target.stat().st_size:
            raise ValueError('Published asset size or checksum did not match; inspect the release before retrying')
        status='Uploaded and verified'
    summary=f"### {status}\n\n[{name}]({asset['browser_download_url']})\n\nSHA-256: `{expected}`\n"
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as output:output.write(summary)
    print(status+': '+name,flush=True)

if __name__=='__main__':
    if sys.argv[1:] not in [['download'],['publish']]:raise SystemExit('Usage: release_asset.py download|publish')
    try:(download if sys.argv[1]=='download' else publish)()
    except (ValueError,RuntimeError,subprocess.CalledProcessError) as error:
        raise SystemExit(str(error))
