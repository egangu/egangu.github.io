# Homepage deployment

## Sites

- Primary server: https://yggu.site, Tencent Cloud Seoul `43.131.235.41`.
- GitHub Pages mirror: https://egangu.github.io. No forced redirect or Pages custom domain is configured.
- Both builds use this repository. `_config.yml` retains the GitHub Pages URL; `_config.seoul.yml` overrides the Seoul build's URL, including canonical links and sitemap.

## Automatic updates

`.github/workflows/deploy-pages.yml` builds the CV PDFs and both Jekyll outputs, then deploys Pages and Seoul. A push to `main`, a successful visits-snapshot workflow, or a manual workflow dispatch starts deployment.

Repository configuration:

- Secret `SEOUL_DEPLOY_KEY`: dedicated SSH private key.
- Variable `SEOUL_DEPLOY_HOST`: server IP.
- Variable `SEOUL_SSH_KNOWN_HOSTS`: host public key obtained over the administrator's authenticated SSH connection.

The `homepage-deploy` account has no sudo access. Its authorized key forces `/usr/bin/rrsync -wo /srv/yggu/homepage/public` with SSH forwarding and PTY disabled. CI can synchronize only the published homepage directory; it cannot run arbitrary server commands or change Caddy configuration. `rsync --delete-delay --delay-updates` removes obsolete published files and delays replacements until transfer finishes; this is not an atomic release switch.

## Server files

```text
/srv/yggu/
├── gateway/
│   ├── config/Caddyfile
│   └── data/               # Caddy-managed certificates and state
└── homepage/
    ├── public/             # CI-published static files
    └── config/README.md
```

The deployment user's SSH authorization is in its `.ssh/` directory, owned by root. Ubuntu package binaries and systemd registration remain in their normal system paths. `/etc/caddy/Caddyfile` points to the gateway config. The systemd drop-in `/etc/systemd/system/caddy.service.d/paths.conf` sets Caddy's writable state paths.

Administrator access from the owner's Mac: `ssh tencent-seoul`.

```bash
sudo systemctl status caddy --no-pager
sudo journalctl -u caddy -n 50 --no-pager
sudo caddy validate --config /srv/yggu/gateway/config/Caddyfile
sudo systemctl reload caddy
```

Infrastructure configuration sources are in `deploy/seoul/` and are not published as website files. Change them through administrator SSH access after validation.

## DNS and HTTPS

Spaceship DNS: `@ A 43.131.235.41`, TTL 300 seconds. Caddy serves the apex domain, redirects HTTP to HTTPS, and renews TLS certificates automatically. Music, Codex and Feilian are outside this deployment.

Domain registration auto-renew is separate from TLS renewal. `yggu.site` registration auto-renew is off; registration expires 2027-11-04. The private domain record is `/Users/yggu/profile/identity/DOMAINS.md`.

## Validation and manual deployment

Check both sites after changing the workflow. On Seoul verify the homepage, CSS, images, both CV PDFs, canonical URLs, sitemap, HTTP-to-HTTPS redirect and a real 404 response. GitHub Pages must continue to return its own content without redirecting to Seoul.

To redeploy the latest `main` without creating another commit:

```bash
gh workflow run deploy-pages.yml --repo egangu/egangu.github.io --ref main
```
