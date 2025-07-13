# Holux M-241 使用指南（Windows 11 & Apple Silicon）

## 前言

Holux M-241 已經停產，原公司亦已解散，僅能從網路上取得相關資訊。  
本頁介紹如何在 Windows 11 及 Apple Silicon（如 MacBook M3）上使用 Holux M-241，包含：

- 安裝驅動程式
- 輸出裝置中的軌跡紀錄
- 在 Windows 上即時讀取 GPS 資訊

---

## Holux M-241 裝置簡介

Holux M-241 採用聯發科 MTK3318 晶片，使用 NMEA0183 v3.1 通訊協定。  
供電方面，可使用單顆 3 號乾電池，續航約 10–12 小時。  
裝置可透過 mini USB 或藍牙連接電腦。  
詳見：[https://holux.info/m-241/](https://holux.info/m-241/)（非官方網站）

---

## Windows 11 / Windows 10

### 驅動程式安裝

由於官方驅動無法取得，可改用 [Silicon Labs](https://www.silabs.com/developer-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads) 提供的 [CP210x 驅動程式](https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip)。

📦 備份載點：  
[CP210x_Windows_Drivers.zip](./CP210x_Windows_Drivers.zip)

安裝方式：

1. 解壓縮檔案
2. 對 `slabvcp.inf` 右鍵 → 選擇「安裝」
3. 插入 M-241 裝置後，應會在 **裝置管理員 > 連接埠（COM 和 LPT）** 看到 `Silicon Labs CP210x` 以及對應的 COM Port

📷 如圖（COM6）  
![Device Manager](./picture/device_manager.PNG)

---

### GPS 軟體工具

來自以下網站：  
[http://4river.a.la9.jp/gps/indexj.htm](http://4river.a.la9.jp/gps/indexj.htm)  
可即開即用，無須安裝：

- **MtkDLut**  
  - 功能：讀取 GPS 狀態、下載/刪除軌跡、重置 GPS 設定（hot/warm/cold）  
  - 📥 備份載點：[MtkDLut336.zip](./MtkDLut336.zip)

- **NMEA2KMZ**  
  - 功能：軌跡格式轉換（KML/KMZ/GPX/NMEA/CSV）  
  - 📥 備份載點：[NMEA2KMZ342.zip](./NMEA2KMZ342.zip)

- **NMEA**  
  - 功能：讀取 GPS 狀態、即時紀錄/重播軌跡  
  - 📥 備份載點：[NMEA407.zip](./NMEA407.zip)

---

## macOS 15（MacBook Air M2/M3）

### 驅動程式安裝（macOS）

同樣可使用 Silicon Labs 的驅動程式：  
[Mac_OSX_VCP_Driver.zip](https://www.silabs.com/documents/public/software/Mac_OSX_VCP_Driver.zip)

📦 備份載點：[macOS_VCP_Driver.zip](./macOS_VCP_Driver.zip)

安裝方式：

1. 解壓縮並掛載 `SiLabsUSBDriverDisk.dmg`
2. 安裝並授權安全性權限（可能需輸入管理者密碼）
3. 裝置連接後，會出現 `/dev/tty.SLAB_USBtoUART`

📷 如圖：  
![macOS USB](./picture/m241_usb_macos.png)

---

### 軟體工具（houdahGPS）

官網：[https://www.houdah.com/houdahGPS/](https://www.houdah.com/houdahGPS/)

免費 GUI 軟體，基於 GPSBabel。下載版本依 macOS 版本選擇：

- macOS 10.10 或更新：  
  [HoudahGPS 8.1.3](https://www.houdah.com/houdahGPS/download_assets/HoudahGPS8.1.3.zip)  
  📥 備份載點：[HoudahGPS8.1.3.zip](./HoudahGPS8.1.3.zip)

- macOS 10.10 以下：  
  [HoudahGPS 6.0](https://www.houdah.com/houdahGPS/download_assets/HoudahGPS6.0.zip)  
  📥 備份載點：[HoudahGPS6.0.zip](./HoudahGPS6.0.zip)

---

### 使用 houdahGPS 匯出軌跡

打開 houdahGPS，設定如下：

- **Preset**：Holux  
- **Port**：USB  
- **Names**：SLAB_USBtoUART（依實際裝置）  
- **Option**：可留空（如勾選將清除裝置軌跡）  
- **Output**：GPX / KML / KMZ（可選）

📷 操作介面示意圖：  
![houdahGPS](./picture/houdahGPS_macos.png)

按下 **Import** 即可下載軌跡資料。

---

## 參考資料

- [OpenStreetMap Wiki - Holux M-241 (JA)](https://wiki.openstreetmap.org/wiki/JA:Holux_M-241)
- [Yamareco 軌跡使用經驗](https://www.yamareco.com/modules/yamanote/detail.php?nid=2428)
- [Ushirotaro 部落格](https://ushirotaro.hatenablog.com/entry/2021/05/23/223821)
- [山2733的 HOLUX 網頁](https://www.katch.ne.jp/~yama2733/Holuxm/HOLUXM.htm)
