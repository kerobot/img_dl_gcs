# img_dl_gcs

Googleカスタム検索APIを利用して画像ファイルをダウンロードします。

事前に Google API KEY と カスタム検索 の 検索エンジンID を用意しておくこと。

## 環境

* Windows 10 x64 1809
* Python 3.6.5 x64
* Power Shell 6 x64
* Visual Studio Code x64
* Git for Windows x64

## 構築

プロジェクトを clone してディレクトリに移動します。

```powershell
> git clone https://github.com/kerobot/img_dl_gcs.git img_dl_gcs
> cd img_dl_gcs
```

プロジェクトのための仮想環境を作成して有効化します。

```powershell
> python -m venv venv
> .\venv\Scripts\activate.ps1
```

念のため、仮想環境の pip をアップグレードします。

```powershell
> python -m pip install --upgrade pip
```

依存するパッケージをインストールします。

```powershell
> pip install -r requirements.txt
```

環境変数を設定します。

> API_KEYとCUSTOM_SEARCH_ENGINEを設定

```powershell
> copy .\.env.sample .\.env
> code .\.env
```

## 実行

検索条件となるキーワードを指定して実行します。

> 10件ごとのクエリを10回実行（最大100ファイル取得）

```powershell
> python .\img_dl_gcs.py 橘南桜,橘莉子,橘咲希
```
