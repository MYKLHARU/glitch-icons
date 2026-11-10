#!/usr/bin/env python3
"""Build a deterministic, versioned ZIP from the validated website manifest."""
from pathlib import Path
from zipfile import ZipFile,ZipInfo,ZIP_DEFLATED
import hashlib,json,os,re,sys

ROOT=Path(__file__).resolve().parents[1]
destination=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'release'
destination.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'docs/manifest.json').read_text())
name=manifest.get('archiveName','Icons-glitch.zip')
assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*\.zip',name)
target=destination/name;temporary=destination/(name+'.tmp')
with ZipFile(temporary,'w',compression=ZIP_DEFLATED,compresslevel=6) as archive:
    archive.writestr(ZipInfo('Icons/',(1980,1,1,0,0,0)),b'')
    for item in sorted(manifest['icons'],key=lambda i:i['file'].casefold()):
        info=ZipInfo('Icons/'+item['file'],(1980,1,1,0,0,0))
        info.compress_type=ZIP_DEFLATED
        archive.writestr(info,(ROOT/'docs/icons'/item['file']).read_bytes(),compresslevel=6)
with ZipFile(temporary) as archive:
    assert len(archive.namelist())==manifest['count']+1
    assert archive.testzip() is None
os.replace(temporary,target)
with target.open('rb') as file:digest=hashlib.file_digest(file,'sha256').hexdigest()
(destination/(name+'.sha256')).write_text(digest+'  '+name+'\n')
print(f'Packaged {manifest["count"]} icons as {name} ({target.stat().st_size:,} bytes)')
