# MateriaRadar · 原料海巡雷達 公開更新通道

提供 **0.3.21** 完整版安裝檔、可攜版、完整資料庫及版本核對資訊。
目前最新為 **2026-10-17 安全修補建置**（`v0.3.21-build.20261017.1`）。
使用者下載與程式內「檢查最新版本」均不需 GitHub 登入、存取權杖或 Python。

- [最新完整安裝版與所有下載](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/latest)
- [最新版本資訊 latest.json](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/latest/download/latest.json)
- [0.3.21 Windows x64 完整版安裝檔](https://github.com/applehitmyhead-svg/MateriaRadar-Updates/releases/latest/download/MateriaRadar-0.3.21-windows-x64-setup.exe)

第一次請下載安裝此通道提供的新版。之後在設定按「檢查最新版本」，
程式會檢查公開版本資訊，有更新即下載、核對 SHA-256、顯示進度並開啟安裝。
同一產品版本有新建置時也可更新；建置相符時顯示「已是最新版本」。
升級沿用使用者資料庫、設定與 Excel 輸出，不以種子強制覆蓋既有資料。

## 完整版內容

Windows x64 安裝檔包含 **512,838 筆完整歷史與修訂紀錄**，以及同一資料快照 **496629**
產生的七本產業明細及價格總表。Excel 副本位於安裝目錄的 Excel 資料夾。
另提供資料庫快照與 manifest，可獨立核對及匯入。
各商品的報價日期按原始來源保留；版本資訊中的資料取得時間不代表全部商品同日報價。

完整版保留酚醛樹脂、碳纖維、雙環戊二烯、順酐及苯酐的公開可核實歷史。
石油化學報表包含「材料完整歷史」分頁，共 4,815 筆實際報價；日／月與不同供應商分列，
沒有可靠報價的日期保持缺口。來源早於目前可取得範圍的歷史不推測填補。

## 本次安全修補

安裝程式內建公開 HTTP／HTTPS 網路限制，拒絕爬蟲連向本機、內網、鏈路本地位址及非標準連接埠，並逐跳驗證轉址與 DNS。
同時限制下載、解壓與遠端 Excel／XML 解析資源，集中遮罩日誌中的可辨識敏感資料，使用 Python 3.14.8 安全修補版本。
安裝版須通過自建本機靶機零請求與公開網站正常連線驗證才發布；舊版需要更新安裝後才會取得這些修補。

## 開源通道工具

tools/generate_manifest.py 僅使用 Python 標準函式庫，依已通過驗證的發行檔案
產生 latest.json，核對 SHA256SUMS、建置 ID、版本與安裝檔。
通道工具及 schema 依本庫 MIT LICENSE 開放；安裝檔、第三方依賴及報價資料沿用各自授權與來源條件。

~~~text
python tools/generate_manifest.py --release-dir path/to/verified-release
~~~

同一產品版本重新封裝時，以不同建置 ID 和 UTC 建立時間識別，避免重複安裝或降版。
重新發佈可使用 --tag v0.3.21-build.YYYYMMDD.BUILD_ID；產品版本仍為 0.3.21。

維護者先上傳安裝檔、資料庫與驗證資訊到草稿 Release，
核對檔案後再上傳相符的 latest.json 並發佈。不要手動修改校驗碼或將不同建置的檔案混用。
終端用戶無需授權；維護者上傳仍使用自己的 GitHub 登入，授權不隨安裝檔散布。
