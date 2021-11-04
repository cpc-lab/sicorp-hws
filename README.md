# Program Classification by PMC & Sklearn SVC
Intel®プロセッサの Performance Monitoring Counter (PMC) を用いて取得したマイクロアーキテクチャイベントの情報をもとにして Support Vector Machine (SVM) によるプログラムの識別を行う．

### （メモ）
判定器部分のスクリプト類は後ほど追加します．\
Readme.md 全体としてかなり適当に作成しているので，ドラスティックに修正します．

## Experimental Setup (for PMC data collectioin)
- Hardware
    - CPU: Intel(R) Xeon(R) CPU E5-2620 v4 @ 2.10GHz (memory 128GB)

- Software 
    - OS: ubuntu 16.04.7 (Linux kernel 4.4.0-194-generic)
    - PMC tool: Linux-perf-tool 4.4.236

### Note
- The following PMC data and 'sudo' are required 
    - 0xC0　INST_RETIRED.ANY_P
    - 0x3C　CPU_CLK_UNHALTED.THREAD_P_ANY
    - 0x81　MEM_UOPS_RETIRED.ALL_LOADS
    - 0x82　MEM_UOPS_RETIRED.ALL_STORES
    - 0xC5　BR_MISP_RETIRED.ALL_BRANCHES

## Other Tools (for analysis & verification):
- g++ 9.3.0
- python 2.8.1 
    - scikit-learn 0.24.2
    - pandas 1.3.1
    - matplotlib 3.4.2

## Repository Structure
```sh
sicorp-hws
├── benchmark
├── cpp
├── data
│   ├── analyze_out
│   ├── arrange_accum_out
│   ├── arrange_delta_out
│   ├── arrange_out
│   ├── norm_param
│   ├── norm_param_f
│   ├── record_out
│   ├── script_out
│   ├── svm_input
│   ├── svm_output
│   └── svm_output_f
└── python
    ├── cpp_out
    ├── cpp_out_f
    └── model
```

- `benchmark/`
    - PMC情報の収集を行うプログラムの実行ファイル

- `data/script_out/ & data/record_out/`
    - perf-tool により取得した生データおよび一時ファイル

- `data/analyze_*/ & data/arrange_*/`
    - perf-tool により取得した生データから必要なものを抽出して整理したデータ
- `data/svm_*`
    - SVM モデルに対する入力用のデータと対応する出力のデータ
- `data/norm_param_*`
    - 特徴量の正規化に用いるパラメータ
- `python/`
    - perf-tool により取得したデータの解析用スクリプト
    - sklearn ライブラリを用いた SVM モデルの生成，PCA等を行うスクリプト
- `python/model/`
    - sklearn ライブラリを用いて生成した SVM モデル
- `python/cpp_out_*/`
    - c++ 実装の SVM の prediction 処理の実行ファイル（検証用）
- `cpp/`
    - c++ による SVM の prediction 処理の実装
- `cpp/h_*`
    - python 実装の SVM モデルから抽出したモデルパラメータ

### Note
- ディレクトリやファイルの分類について 
    - 何も書いてない or section 区間毎方式
    - accum 累積和方式
    - delta 変化量方式
&#13;&#10;
- 末尾に f 付きのものは float 実装（32bit），それ以外は double 実装（64 bit）

## Experiment FLow
適宜，実行時に必要なコマンドライン引数をシェルスクリプトにまとめています．
   1. `run_perf.sh` （perf-tool によるデータの収集）
   2. `python/analyze_arrange_*.sh` （データの整理）
        - `python/analyze.py`
        - `python/arrange_*.py`
   3. `python/pca.sh`　（主成分分析）
        - `python/pca.py`
   4. `python/mkall.sh` （モデル生成，パラメータ抽出，c++ 検証用データの生成）
        - `python/mkmodel_hex.py`
        - `python/mkheader_hex.py`
        - `python/mktest_hex.py`
   5. `cpp/mk_acc_*.sh` （c++ 実装の SVM のコンパイル）
        - `cpp/mk_acc.cpp`
        - `cpp/mk_acc_f.cpp`
   6. `python/acc_hex_*.sh` （モデルの識別精度の確認）
        - `python/acc_hex.py`
        - `python/acc_hex_f.py`