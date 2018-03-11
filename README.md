自用的vapoursynth模板

源滤镜：DGNV，L-SMASH，FFMS2000。

处理滤镜和脚本：
1.截取（Trim）
2.反交错（QTGMC）
3.反交错(DGNV）
4.反胶卷过带（VS）
5.反胶卷过带（DGNV）
6.帧率改变 ChangeFPS和AssumeFPS
7.HDR to SDR(tonemap)
8.降噪（KNLMeansCL）
9.降噪（SMDegrain）
11.SVP补帧
12.DGNV处理滤镜（降噪和锐化）
13.Deblocking
14.Debanding
15.黑边处理
16.字幕
17.分辨率调整和修改色彩标准（gamma-aware）
18.NNEDI3_resize16的分辨率放大
19.补偿性锐化（LSFmod和Awarpsharp2）
20.位深改变（fmtc.bitdepth）
...

releases里是自用的VS滤镜和脚本包，可选择性使用。
