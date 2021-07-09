# Bitalino (r)evolution + matplotlib + pandas

Bitalino (r)evolution で計測する生体信号の波形表示，および記録した信号のExcelファイルへのエクスポート

# Requirement

* [BITalino (r)evolution Python API](https://github.com/BITalinoWorld/revolution-python-api)
* matplotlib
* Pandas

# Usage
Bitalinoとペアリングをしておくこと．

## 実行

```bash
python ADmonirecBitalino.py <Channels> <Fs> <Trec>
```
ここで
- Channels: 測定するチャンネル(A1-A5)の設定．カッコ( )内はBoard Kitの場合
    - 0: A1 (EMG)
    - 1: A2 (ECG)
    - 2: A3 (EDA)
    - 3: A4 (EEG)
    - 4: A5 (ACC)
- Fs: サンプリング周波数 (≦1000) [Hz] 
- Trec: Rキーの押下時刻を開始時刻としたデータの収録時間[s]

例えば
```bash
python ADmonirecBitalino.py 0 1 3 1000 5.0
```
は，A1, A2, A4チャンネルを使用して，Fs=1000[Hz]，収録時間を5[s]とする．

## 波形表示時の操作
* Qキーを押すと終了
* Rキーを押した時点から記録開始，波形画面はフリーズする．Trec秒記録を行い，終了する．
