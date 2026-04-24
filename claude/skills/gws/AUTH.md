# gws 授權設定（使用 gcloud，不需自建 OAuth client）

`gws` 預設需要自建 OAuth client，但可透過 `GOOGLE_WORKSPACE_CLI_TOKEN` 環境變數直接帶 access token，繞過本地憑證流程。搭配 gcloud 是最快的方式。

## 一次性授權

```bash
gcloud auth login --enable-gdrive-access
```

## 每個 shell session 使用前

```bash
export GOOGLE_WORKSPACE_CLI_TOKEN=$(gcloud auth print-access-token)
gws sheets spreadsheets get --params '{"spreadsheetId": "..."}'
```

## 其他授權方式（參考）

- https://github.com/googleworkspace/cli#authentication
