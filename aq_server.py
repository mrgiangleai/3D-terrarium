#!/usr/bin/env python3
"""Máy chủ nhỏ cho Bể Cá 3D.

- Phục vụ các file trong thư mục này (chỉ lắng nghe 127.0.0.1, không ra ngoài mạng).
- API quản lý mô hình 3D: danh mục, xóa file, tải mô hình Poly Haven, tìm Sketchfab, thư mục inbox.
Chạy:  python3 aq_server.py 8791
"""
import http.server, socketserver, json, os, sys, subprocess, shutil, urllib.parse, re, threading

ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.join(ROOT, 'models')
CATALOG = os.path.join(MODELS, 'catalog.json')
INBOX = os.path.join(MODELS, 'inbox')
PH_API = 'https://api.polyhaven.com'
LOCK = threading.Lock()


def curl_json(url, timeout=60):
    r = subprocess.run(['curl', '-s', '-f', '-A', 'Mozilla/5.0', url], capture_output=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError('Không kết nối được: %s' % url)
    return json.loads(r.stdout)


def curl_file(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    r = subprocess.run(['curl', '-s', '-f', '-L', '-o', dest, url], timeout=900)
    if r.returncode != 0:
        raise RuntimeError('Tải lỗi: %s' % url)


def safe(rel):
    """Đường dẫn tuyệt đối nằm trong thư mục models (chặn ../)."""
    p = os.path.normpath(os.path.join(MODELS, rel))
    if p == MODELS or not p.startswith(MODELS + os.sep):
        raise ValueError('Đường dẫn không hợp lệ: %s' % rel)
    if os.path.basename(p) == 'catalog.json':
        raise ValueError('Không được xóa danh mục')
    return p


def path_size(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    t = 0
    for d, _, fs in os.walk(p):
        for f in fs:
            try:
                t += os.path.getsize(os.path.join(d, f))
            except OSError:
                pass
    return t


def ph_gltf(aid):
    if not re.fullmatch(r'[A-Za-z0-9_\-]+', aid):
        raise ValueError('id không hợp lệ')
    g = curl_json('%s/files/%s' % (PH_API, aid))['gltf']
    res = '1k' if '1k' in g else sorted(g.keys())[0]
    return g[res]['gltf']


def gltf_nodes(path):
    """Danh sách node có mesh (tên + kích thước mét) để tạo từng mục trong thư viện."""
    g = json.load(open(path))
    acc = g['accessors']
    out = []
    for ni in g['scenes'][0]['nodes']:
        n = g['nodes'][ni]
        if 'mesh' not in n:
            continue
        a = acc[g['meshes'][n['mesh']]['primitives'][0]['attributes']['POSITION']]
        sc = n.get('scale', [1, 1, 1])
        out.append({'name': n.get('name', 'node%d' % ni),
                    'size': [(a['max'][i] - a['min'][i]) * sc[i] for i in range(3)]})
    return out


class H(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json', '.mjs': 'text/javascript'}

    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    # ---- helpers ----
    def send_json(self, obj, code=200):
        b = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def body(self):
        n = int(self.headers.get('Content-Length') or 0)
        return json.loads(self.rfile.read(n) or b'{}')

    def fail(self, e, code=500):
        self.send_json({'error': str(e)}, code)

    # ---- routes ----
    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if not u.path.startswith('/api/'):
            return super().do_GET()
        q = urllib.parse.parse_qs(u.query)
        try:
            if u.path == '/api/ping':
                return self.send_json({'ok': True})
            if u.path == '/api/catalog':
                if not os.path.exists(CATALOG):
                    return self.send_json({'error': 'chưa có danh mục'}, 404)
                return self.send_json(json.load(open(CATALOG)))
            if u.path == '/api/sizes':
                out = {}
                if os.path.isdir(MODELS):
                    for n in os.listdir(MODELS):
                        if n == 'catalog.json' or n.startswith('.'):
                            continue
                        p = os.path.join(MODELS, n)
                        out[n] = path_size(p)
                        if n in ('fish', 'inbox') and os.path.isdir(p):
                            for d, _, fs in os.walk(p):
                                for fn in fs:
                                    fp = os.path.join(d, fn)
                                    out[os.path.relpath(fp, MODELS)] = os.path.getsize(fp)
                return self.send_json(out)
            if u.path == '/api/phinfo':
                g = ph_gltf(q['id'][0])
                total = g['size'] + sum(v['size'] for v in g['include'].values())
                return self.send_json({'id': q['id'][0], 'bytes': total})
            if u.path == '/api/sf':
                qs = urllib.parse.urlencode({'type': 'models', 'q': q.get('q', [''])[0], 'downloadable': 'true',
                                             'count': 24, 'sort_by': '-likeCount'})
                d = curl_json('https://api.sketchfab.com/v3/search?' + qs)
                res = []
                for m in d.get('results', []):
                    imgs = sorted(m.get('thumbnails', {}).get('images', []), key=lambda i: abs(i['width'] - 256))
                    res.append({'uid': m['uid'], 'name': m['name'], 'author': (m.get('user') or {}).get('displayName', ''),
                                'license': (m.get('license') or {}).get('label', '?'), 'faces': m.get('faceCount'),
                                'url': m.get('viewerUrl'), 'thumb': imgs[0]['url'] if imgs else '',
                                'animated': bool(m.get('animationCount'))})
                return self.send_json(res)
            if u.path == '/api/inbox':
                os.makedirs(INBOX, exist_ok=True)
                files = []
                for d, _, fs in os.walk(INBOX):
                    for f in fs:
                        if f.lower().endswith(('.glb', '.gltf')):
                            p = os.path.join(d, f)
                            files.append({'path': os.path.relpath(p, MODELS), 'bytes': os.path.getsize(p)})
                return self.send_json(files)
            return self.send_json({'error': 'không có API này'}, 404)
        except Exception as e:
            return self.fail(e)

    def do_PUT(self):
        if self.path != '/api/catalog':
            return self.send_json({'error': 'không có API này'}, 404)
        try:
            data = self.body()
            os.makedirs(MODELS, exist_ok=True)
            with LOCK:
                tmp = CATALOG + '.tmp'
                json.dump(data, open(tmp, 'w'), ensure_ascii=False, indent=1)
                os.replace(tmp, CATALOG)
            return self.send_json({'ok': True})
        except Exception as e:
            return self.fail(e)

    def do_POST(self):
        try:
            b = self.body()
            if self.path == '/api/delete':
                freed = 0
                for rel in b.get('paths', []):
                    p = safe(rel)
                    if os.path.exists(p):
                        freed += path_size(p)
                        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
                return self.send_json({'freed': freed})
            if self.path == '/api/polyhaven':
                aid = b['id']
                g = ph_gltf(aid)
                base = safe(aid)
                if os.path.exists(base):
                    shutil.rmtree(base)
                curl_file(g['url'], os.path.join(base, aid + '.gltf'))
                for rel, v in g['include'].items():
                    curl_file(v['url'], os.path.join(base, rel))
                nodes = gltf_nodes(os.path.join(base, aid + '.gltf'))
                return self.send_json({'id': aid, 'url': '%s/%s.gltf' % (aid, aid), 'nodes': nodes, 'bytes': path_size(base)})
            if self.path == '/api/open':
                p = safe(b['path']) if b.get('path') != 'inbox' else INBOX
                os.makedirs(p, exist_ok=True)
                subprocess.Popen(['open', p])
                return self.send_json({'ok': True})
            return self.send_json({'error': 'không có API này'}, 404)
        except Exception as e:
            return self.fail(e)


class S(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8791
    os.makedirs(INBOX, exist_ok=True)
    S(('127.0.0.1', port), H).serve_forever()
