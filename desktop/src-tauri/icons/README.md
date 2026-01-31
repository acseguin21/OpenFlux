# App icons

Add your app icons here for the Tauri bundle:

- **32x32.png** – 32×32 PNG
- **128x128.png** – 128×128 PNG
- **icon.icns** – macOS app icon (e.g. from 32, 128, 256, 512)
- **icon.ico** – Windows icon (multi-size)

Without these, `tauri build` may fail. You can generate them from a single source image using [Tauri’s icon guide](https://v2.tauri.app/develop/icons/) or tools like `iconutil` (macOS) and ImageMagick.

For a quick local build without custom icons, you can temporarily remove or comment out the `bundle.icon` array in `tauri.conf.json` and use Tauri’s default (if your Tauri version provides one), or add minimal placeholder PNGs.
