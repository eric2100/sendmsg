# SendMsg

使用 Telegram Bot API 發送文字及檔案的 Bash 腳本，支援官方與自架 Bot API 伺服器。

## 需求

- Bash 和 curl
- Telegram Bot token，以及已允許 Bot 發送訊息的聊天 ID

## 設定及使用

請透過安全方式設定環境變數，不要把真實憑證提交至 Git：

```bash
export TELEGRAM_BOT_TOKEN="你的 Bot token"
export TELEGRAM_CHAT_ID="你的聊天 ID"
./SendMsg "測試訊息"
./SendMsg "備份完成" "/path/to/backup.tar.gz"
```

預設使用 Telegram 官方 API。若要使用自架 API：

```bash
export TELEGRAM_API_BASE_URL="http://127.0.0.1:8081"
./SendMsg "測試訊息"
```

遠端連線應使用 HTTPS 並驗證伺服器憑證。自簽憑證可以使用 `CURL_CA_BUNDLE` 指定受信任的憑證檔，請透過可信管道取得及驗證憑證。

官方 Bot API 檔案上限為 50 MB；自行架設並啟用 local mode 可上傳至 2000 MB。實際上限依 Telegram 官方服務為準。

## 測試

```bash
python3 -m unittest discover -s tests -v
```

測試使用假的 curl，不會傳送訊息或連接 Telegram。
