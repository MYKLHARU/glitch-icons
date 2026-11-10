#!/usr/bin/env python3
"""Apply tracked website updates to the published base-site archive."""
from pathlib import Path
import hashlib,json,os,re,shutil,struct,sys,zlib

HERE=Path(__file__).resolve().parent
REPOSITORY=HERE.parent
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('glitch-icons').resolve()
DOCS=ROOT/'docs'
updates=json.loads((HERE/'updates.json').read_text())

def chunk(kind,payload):
    return struct.pack('>I',len(payload))+kind+payload+struct.pack('>I',zlib.crc32(kind+payload)&0xffffffff)

def full_return(data):
    # Keep the five approved frames, then copy the first compressed frame into
    # a full-canvas return frame. This preserves pixels and the pack's validator.
    chunks=[];offset=8
    while offset<len(data):
        size=struct.unpack_from('>I',data,offset)[0]
        kind=data[offset+4:offset+8];payload=data[offset+8:offset+8+size]
        assert zlib.crc32(kind+payload)&0xffffffff==struct.unpack_from('>I',data,offset+8+size)[0]
        chunks.append((kind,payload));offset+=12+size
    assert offset==len(data)
    first_data=[payload for kind,payload in chunks if kind==b'IDAT']
    controls=[i for i,(kind,_) in enumerate(chunks) if kind==b'fcTL']
    assert len(controls)==6
    last=controls[-1];control=list(struct.unpack('>IIIIIHHBB',chunks[last][1]))
    control[1:]=[320,180,0,0,2,1,0,0]
    result=data[:8]+b''.join(chunk(k,p) for k,p in chunks[:last])
    result+=chunk(b'fcTL',struct.pack('>IIIIIHHBB',*control))
    for index,payload in enumerate(first_data,start=control[0]+1):
        result+=chunk(b'fdAT',struct.pack('>I',index)+payload)
    return result+chunk(b'IEND',b'')

manifest_path=DOCS/'manifest.json'
manifest=json.loads(manifest_path.read_text())
catalog={item['file']:item for item in manifest['icons']}
for entry in updates['icons']:
    name=entry['file'];assert Path(name).name==name
    target=DOCS/'icons'/name
    target.write_bytes(full_return((REPOSITORY/entry['source']).read_bytes()))
    shutil.copyfile(REPOSITORY/entry['still'],DOCS/'stills'/name)
    catalog[name]={'file':name,'name':entry['name'],'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'addedAt':entry['addedAt']}
manifest['icons']=sorted(catalog.values(),key=lambda item:item['file'].casefold())
manifest['count']=len(catalog);manifest['archiveName']=updates['packAsset']
manifest_path.write_text(json.dumps(manifest,separators=(',',':'))+'\n')
(DOCS/'catalog.js').write_text('window.GLITCH_CATALOG = '+json.dumps(manifest['icons'],separators=(',',':'))+';\n')

for name in ['app.js','sort.js']:shutil.copyfile(HERE/name,DOCS/name)
repo=os.environ.get('SITE_REPOSITORY','MYKLHARU/glitch-icons')
config={'repository':repo,'apkAsset':updates['apkAsset'],'packAsset':updates['packAsset']}
(DOCS/'config.js').write_text('window.GLITCH_CONFIG = '+json.dumps(config)+';\n')
html=DOCS/'index.html';content=html.read_text()
content=content.replace('1,195',format(manifest['count'],','))
if 'value="newest"' not in content:
    content=content.replace('<option value="featured">Featured first</option>','<option value="featured">Featured first</option><option value="newest">Newest first</option>')
content=content.replace('Glitch-Reflections.apk',updates['apkAsset']).replace('Icons-glitch.zip',updates['packAsset'])
content=content.replace('https://github.com/'+repo+'/releases/latest/download/'+updates['packAsset'],'downloads/'+updates['packAsset'])
content=content.replace('Download APK','Download TV APK').replace('~217 MB','~218 MB')
content=content.replace('These files keep their original .png filenames while containing six animation frames.','Most files keep their original .png filenames; .apng files use the same animated PNG format. Each contains six animation frames.')
build=os.environ.get('SITE_BUILD','local')
sort_script='<script src="sort.js?v='+build+'" defer></script>'
if re.search(r'<script src="sort\.js[^\"]*" defer></script>',content):
    content=re.sub(r'<script src="sort\.js[^\"]*" defer></script>',sort_script,content)
else:
    content=content.replace('<script src="app.js',sort_script+'\n  <script src="app.js',1)
html.write_text(content)

# Preserve all PNG/sequence/CRC/hash checks while allowing new .apng filenames
# and a catalogue whose count grows as icons are added.
validator=ROOT/'tools/validate_pack.py';text=validator.read_text()
text=text.replace("assert len(manifest['icons']) == manifest['count'] == 1195","assert len(manifest['icons']) == manifest['count'] and manifest['count'] >= 1195")
text=text.replace("{p.name for p in (ROOT/'docs'/'icons').glob('*.png')}","{p.name for p in (ROOT/'docs'/'icons').iterdir() if p.suffix.lower() in ('.png','.apng')}")
text=text.replace("print('Validated 1,195 icons:","print(f'Validated {manifest[\"count\"]:,} icons:")
validator.write_text(text)
shutil.copyfile(HERE/'package_pack.py',ROOT/'tools/package_release.py')
print(f'Website updated: {manifest["count"]:,} icons; Newest first; {updates["apkAsset"]}; {updates["packAsset"]}')
