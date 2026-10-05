"""Minimal Minecraft RCON client for the local dev server (gradlew runServer, folder run-server/).

Host, port and password come from run-server/server.properties (setup-main-pc.ps1 turns RCON on there).

usage: python tools/dev/rcon.py "command"            run one command, print the reply
       python tools/dev/rcon.py --file commands.txt  run every line (blank lines and # comments skipped), print failures
"""
import os, socket, struct, sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SERVER_DIR = os.path.join(REPO, 'run-server')


def server_properties():
    props = {}
    path = os.path.join(SERVER_DIR, 'server.properties')
    if not os.path.exists(path):
        raise SystemExit(f"{path} not found: run the server once (gradlew runServer) or tools/dev/setup-main-pc.ps1")
    for line in open(path, encoding='utf-8'):
        if '=' in line and not line.startswith('#'):
            k, v = line.rstrip('\n').split('=', 1)
            props[k] = v
    return props


class Rcon:
    def __init__(self):
        props = server_properties()
        if props.get('enable-rcon') != 'true' or not props.get('rcon.password'):
            raise SystemExit("RCON is off: set enable-rcon=true and rcon.password in run-server/server.properties")
        self.s = socket.create_connection(('127.0.0.1', int(props.get('rcon.port', 25575))), timeout=1500)
        self.req = 0
        if self._send(3, props['rcon.password'])[0] == -1:
            raise SystemExit("RCON login failed")

    def _send(self, kind, body):
        self.req += 1
        data = struct.pack("<ii", self.req, kind) + body.encode("utf-8") + b"\x00\x00"
        self.s.sendall(struct.pack("<i", len(data)) + data)
        size = struct.unpack("<i", self._read(4))[0]
        rid, _ = struct.unpack("<ii", self._read(8))
        return rid, self._read(size - 8)[:-2].decode("utf-8", "replace")

    def _read(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.s.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("RCON closed")
            buf += chunk
        return buf

    def cmd(self, command):
        return self._send(2, command)[1]


if __name__ == "__main__":
    r = Rcon()
    if sys.argv[1] == "--file":
        lines = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#")]
        bad = 0
        for line in lines:
            reply = r.cmd(line)
            low = reply.lower()
            if any(w in low for w in ("unknown", "incorrect", "expected", "invalid", "error", "not loaded", "too many")):
                bad += 1
                if bad <= 15:
                    print("FAIL:", line[:110], "->", reply[:160])
        print(f"ran {len(lines)} commands, {bad} failed")
    else:
        print(r.cmd(" ".join(sys.argv[1:])))
