# Upload Orbit 3DS to GitHub using only the browser

1. Download `orbit3ds-cloud-build-kit.zip` and open the Chromebook **Files** app.
2. Open **Downloads**, right-click the ZIP, and choose **Extract all**.
3. In your browser, open GitHub and create a new empty repository. A good name is `orbit-3ds`. Do not add a README, license, or `.gitignore` during repository creation.
4. Open the new repository and choose **Add file → Upload files**.
5. From the extracted folder, upload the project contents: `index.html`, `README.md`, `UPLOAD-GUIDE.md`, the `core` folder, the `scripts` folder, and the `.github` workflow folder. Then commit to `main`.
6. If the Chromebook file picker hides `.github`, use **Add file → Create new file** in GitHub. Enter this exact path as the filename: `.github/workflows/verify-and-deploy.yml`. Open `GITHUB-WORKFLOW-COPY-THIS.yml` from the extracted folder, copy its contents, paste them into the new GitHub file, and commit. You can skip uploading the hidden `.github` folder in step 5 if you use this fallback.
7. In the repository, open **Settings → Pages**. Under **Build and deployment**, set **Source** to **GitHub Actions**.
8. Open **Actions** and look for **Verify and deploy Orbit 3DS**. A green check means the HTML passed validation and the shell was published. Open the deployment details to find the Pages URL.

If the workflow fails, open its run, select the failed step, and share the error text (not passwords or private keys). Do not share your GitHub password or Firebase service-account credentials.
