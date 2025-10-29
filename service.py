cat > ~/.kodi/addons/service.boot-matrixfx/service.py <<'EOF'
# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon
import random, time

ADDON  = xbmcaddon.Addon(id="service.boot-matrixfx")
LOGTAG = "[service.boot-matrixfx] "

def log(msg, level=xbmc.LOGINFO):
    xbmc.log(LOGTAG + str(msg), level)

def get_float(key, fallback):
    try:
        v = ADDON.getSetting(key)
        return float(v) if v else fallback
    except Exception:
        return fallback

def get_int(key, fallback):
    try:
        v = ADDON.getSetting(key)
        return int(float(v)) if v else fallback
    except Exception:
        return fallback

class RainWindow(xbmcgui.WindowDialog):
    def __init__(self, secs=8.0, columns=48, speed_px=18, font="font13"):
        super().__init__()
        self.duration = max(0.5, float(secs))
        self.columns  = max(1, int(columns))
        self.speed    = max(1, int(speed_px))
        self.font     = font or "font13"

        self.w = self.getWidth()
        self.h = self.getHeight()

        # Tight glyph set (fullwidth katakana + digits + A–Z) with no spaces
        self.glyphs = u"ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.col_w = max(10, self.w // self.columns)
        self.controls, self.state = [], []

        # black backdrop
        bg = xbmcgui.ControlImage(0, 0, self.w, self.h, "")
        self.addControl(bg)
        bg.setColorDiffuse("FF000000")

        self._init_columns()

    def _rand_string(self, n):
        return u"".join(random.choice(self.glyphs) for _ in range(n))

    def _init_columns(self):
        for i in range(self.columns):
            x = i * self.col_w + (self.col_w // 8)
            length = random.randint(8, 22)
            label  = self._rand_string(length)
            y = random.randint(-self.h, 0)
            ctl = xbmcgui.ControlLabel(
                x, y, self.col_w, self.h + 200, label,
                font=self.font, textColor="55A8FF55", alignment=0x00000002
            )
            self.addControl(ctl)
            self.controls.append(ctl)
            self.state.append([y, length])

    def _tick(self):
        for idx, ctl in enumerate(self.controls):
            y, length = self.state[idx]
            y += self.speed
            if y > self.h:
                y = random.randint(-self.h // 2, -20)
                length = random.randint(8, 22)
                ctl.setLabel(self._rand_string(length))
                # subtle head highlight sometimes
                ctl.setTextColor("55A8FF55" if random.random() > 0.3 else "88CCFF88")
            ctl.setPosition(ctl.getX(), y)
            self.state[idx][0] = y
            self.state[idx][1] = length

    def run(self):
        t0 = time.time()
        xbmc.executebuiltin('Action(HideOSD)')
        mon = xbmc.Monitor()
        while (time.time() - t0) < self.duration and not mon.abortRequested():
            self._tick()
            xbmc.sleep(16)  # ~60fps

    def onAction(self, action):
        # any key/touch closes early
        self.close()

class Service(xbmc.Monitor):
    def run(self):
        log("service starting")
        # Wait for Kodi home so we have a surface
        while not xbmc.getCondVisibility("Window.IsVisible(home)"):
            if self.abortRequested():
                log("aborted before home")
                return
            xbmc.sleep(150)
        xbmc.sleep(400)  # tiny settle
        secs  = get_float("duration", 8.0)
        cols  = get_int("columns", 48)
        speed = get_int("speed_px", 18)
        font  = ADDON.getSetting("font") or "font13"
        log(f"starting rain: secs={secs} cols={cols} speed={speed} font={font}")
        win = RainWindow(secs, cols, speed, font)
        try:
            win.show()
            win.run()
        finally:
            try:
                win.close()
            except:
                pass
        log("service finished")

if __name__ == "__main__":
    Service().run()
EOF
chmod 755 ~/.kodi/addons/service.boot-matrixfx/service.py
