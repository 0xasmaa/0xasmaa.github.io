# Medium feed setup

This portfolio includes a Python script and GitHub Actions workflow to sync recent public Medium posts.

1. Upload the **contents** of this folder to the root of `0xasmaa.github.io`, merging/replacing matching files.
2. Keep GitHub Pages publishing from `main` / `(root)` if that is your existing setup.
3. Open Actions → Update Medium articles → Run workflow.
4. On success, `_data/medium_posts.json` will contain the latest posts; the homepage and Writing page read that file.

The workflow checks daily at 06:23 UTC. Medium or GitHub may delay scheduled jobs.
