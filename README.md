自用的vapoursynth模板

源滤镜：DGNV，L-SMASH，FFMS2000。

处理滤镜和脚本：  
1.截取（Trim）  
2.反交错（QTGMC DGNV）  
3.反胶卷过带（VIVTC DGNV）  
4.旋转（Transpose FlipHorizontal FlipVertical）  
5.帧率改变（ChangeFPS AssumeFPS VFRtoCFR）  
6.HDRtoSDR（tonemap.Hable tonemap.Mobius）  
7.降噪（KNLmeansCL SMDegrain BM3D）  
8.补帧（SVP）  
9.DeBolcking（Deblock_QED）  
10.DeBanding（f3kdb）  
11.黑边处理（CropRel AddBorders）  
12.硬字幕（sub.TextFile sub.ImageFile vsfm.TextSubMod）  
13.调色（adjust）  
14.高质量分辨率缩放（线性光各种算法缩小，nnedi3resample等各种高级算法放大，支持修改视频色域属性）  
15.锐化（awarpsharp2 LSFmod）  
16.输出位深改变（fmtc.bitdepth）  

更多功能欢迎下载脚本查看。  


自用VS滤镜和脚本收集：https://1drv.ms/f/s!AnNR9fAbPdHFolsh-kHl_JTiZRB9  

描述：对mawen 20170511的滤镜收集进行更新，并且添加新滤镜，删掉一些我用不到的滤镜。    
感谢mawen大佬和众多滤镜和脚本的作者。  
