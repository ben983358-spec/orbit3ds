# Orbit 3DS — browser-only cloud build starter

This package is intended for a Chromebook workflow with **no Linux, terminal, Rust, CMake, or local compiler setup**.

## What is included

- `index.html` — the Orbit 3DS browser shell (dual screens, importable local game library, virtual controls, IndexedDB save-file backups, and Firebase sign-in/cloud save-file backup wiring).
- `.github/workflows/verify-and-deploy.yml` — GitHub Actions validation and GitHub Pages deployment. GitHub's hosted runner does the checks and publishes the site.
- `scripts/verify_project.py` — checks required interface elements and parses the inline JavaScript with Node.js on the hosted runner.
- `core/README.md` and `core/adapter-contract.json` — documents the future WebAssembly core integration boundary.

## Important: this does not build the 3DS emulator core yet

As checked on 2026-10-30, a developer has demonstrated a Panda3DS-based browser experiment using WebAssembly for ARM recompilation and WebGL2 for graphics. The developer's status page says the public player is offline while the next version is prepared, and that the source will return with that release. The linked source repository currently returns 404. See:

- Browser-port status: <https://panda.profy.top/>
- Developer's technical write-up: <https://dev.to/yury_gagarin_b26c9247af7c/nintendo-3ds-in-a-browser-two-days-of-ai-assisted-porting-then-the-hard-parts-3ai2>
- Main Panda3DS source: <https://github.com/wheremyfoodat/Panda3DS>

The ordinary Panda3DS desktop repository does not currently expose an Emscripten build target in its top-level CMake configuration. A GitHub Actions runner can compile code, but it cannot create the missing browser-specific CPU, renderer, audio, input, and filesystem adaptations automatically. This starter therefore validates and deploys Orbit's shell; it does **not** claim to compile a usable emulator core.

Do not add desktop `.exe`, `.dll`, `.so`, or native Panda3DS builds to `core/` and expect Chrome to run them. The eventual core must be an actual browser build with its JavaScript loader and `.wasm` asset, plus a bridge matching `core/adapter-contract.json`.

## Upload this project to GitHub without a terminal

1. Download and extract this ZIP using the Chromebook Files app.
2. In GitHub, create a **new empty repository** named `orbit-3ds` (or another name you choose). Do not initialize it with a README or license because this package already contains files.
3. Open the new repository, choose **Add file → Upload files**, and upload the extracted project contents. Make sure `.github/workflows/verify-and-deploy.yml` is included. If GitHub's uploader hides dot-folders, create `.github/workflows` with **Add file → Create new file** and create `verify-and-deploy.yml` there, then paste the workflow from this package.
4. Commit the uploaded files to the `main` branch.
5. Open **Settings → Pages** and set the publishing source to **GitHub Actions**.
6. Open the **Actions** tab. The workflow will validate the HTML and deploy the shell to GitHub Pages. It should show a page URL when deployment succeeds.

After that, updates are just browser uploads/commits in GitHub. GitHub Actions performs the validation and deployment remotely.

## Firebase notes

The prototype uses the existing Firebase web-app configuration found in the saved NexOS project and a namespaced path under `users/{uid}/emulator3ds/`. The Firebase web API key is a public client identifier, not an Admin credential. Never put a Firebase service-account JSON, private key, or Admin SDK credential in `index.html`, GitHub Pages, or any browser bundle.

Cloud save uploads require your Firebase project to have:

- Email/password Authentication enabled (or the sign-in provider you use).
- Realtime Database rules granting a signed-in user access only to their own `users/{uid}/emulator3ds` metadata.
- Storage rules granting a signed-in user access only to their own `users/{uid}/emulator3ds/**` files.
- The site hostname authorized in Firebase Authentication.

For Realtime Database, the intended rule shape is:

```json
{
  "rules": {
    "users": {
      "$uid": {
        "emulator3ds": {
          ".read": "auth != null && auth.uid === $uid",
          ".write": "auth != null && auth.uid === $uid"
        }
      }
    }
  }
}
```

For Firebase Storage, merge this match into your existing Storage rules:

```javascript
match /users/{userId}/emulator3ds/{allPaths=**} {
  allow read, write: if request.auth != null && request.auth.uid == userId;
}
```

These snippets show the intended per-user boundary; they are examples to merge, not a replacement for your full existing rules. Do not replace your existing database or Storage rules wholesale. Test with a separate account before storing important saves. The project has not been connected to or tested against your live Firebase rules from this package.

## Save-system limits in this stage

- IndexedDB stores imported game files and imported/exported save-file backups locally.
- Firebase Storage stores selected uploaded save-file backup blobs; Realtime Database stores their metadata.
- True emulator autosaves and full save states cannot work until a real emulator core exposes save-data serialization. The current UI's save-state backup is only a file import/export container, not a generated emulator snapshot.
- The browser prototype does not upload game cartridges to Firebase.

## Testing after deployment

First test the app without any game file: open it, navigate between tabs, request persistent browser storage, and verify no startup errors. Next, use a legally obtained homebrew/test file for library import and test importing/exporting a harmless sample save file. Do not treat the app as a working 3DS emulator until the core status changes to connected and the core's compatibility is independently verified.

For a browser-only upload walkthrough, see `UPLOAD-GUIDE.md`. A visible copy of the workflow is also included as `GITHUB-WORKFLOW-COPY-THIS.yml` in case the Chromebook file picker hides the `.github` folder.
