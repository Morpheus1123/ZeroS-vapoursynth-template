import vapoursynth as vs
import havsfunc as haf
#import mvsfunc as mvf
#import nnedi3_resample as nnrs
#import sys
#import adjust
#import avsfunc
#import finedehalo
#import finesharp
#import hysteria
#import MCDenoise
#import muvsfunc as muf
#import vsTAAmbk
#import xvsfunc as xvf

#threads：设置vs使用的cpu线程数。accept_lowercase：设置"True"和"False"是否支持小写。max_cache_size：设置vs使用的帧缓冲区大小（MB）。
core = vs.get_core(accept_lowercase=True,threads=8)
core.max_cache_size = 12000

#源滤镜（L-SMASH）
#LibavSMASHSource适用于MP4格式，不需要做索引，可以快速打开。LWLibavSource适用于其他格式，需要等待制作索引。
#在fpsnum=0,fpsden=1处填写帧率，可将VFR转换为CFR。遇到滤镜将视频帧率识别错误的情况，不要使用此参数，会造成音画不同步。要使用AssumeFPS修复帧率。
#decoder参数可以选择解码器，默认（留空）为软解。遇到h264或h265，并且你的N卡支持硬解该格式的视频流，可以填写h264_cuvid或h265_cuvid。I卡则填写h264_qsv...其他硬解解码器请参考FFMPEG的-codecs说明。
#注意：部分MP4及其派生格式缺少索引信息，若用LibavSMASHSource则会遇到帧准确性不足的问题。比较稳妥的办法是所有视频都用LWLibavSource打开，代价是要等待制作索引。
src = core.lsmas.LWLibavSource(source="G:/DGNVindex/AAA/AAA.mkv",fpsnum=0,fpsden=1,decoder="")
#src = core.lsmas.LibavSMASHSource(source="G:/DGNVindex/AAA/AAA.mp4",fpsnum=0,fpsden=1,decoder="")

#源滤镜（DGNV-VS）
#选择64位DGDecodeNV.dll和DGI的位置。
#fieldop=0表示遵循Pulldown Flags，1是强制pulldown，2是什么都不做。deinterlace=0为不反交错，1为普通反交错，2为倍帧反交错。可以使用DGNV内置的裁剪和缩放滤镜，速度非常快，质量一般。处理顺序是：去隔行，裁剪，缩放。
#注意：DGNV的VS模式目前不完善，部分内置处理滤镜无法使用。若需要使用，请使用AVS模式。详情参考vapoursynth note和DNGV支持论坛。
#core.std.LoadPlugin("C:/Program Files/dgdecnv/x64 Binaries/DGDecodeNV.dll")
#src = core.dgdecodenv.DGSource("G:/DGNVindex/AAA/AAA.dgi",fieldop=2,deinterlace=0,crop_t=0,crop_b=0,crop_l=0,crop_r=0,resize_w=0,resize_h=0,fulldepth=True)

#源滤镜（DGNV-AVS）
#选择64位DGDecodeNV.dll和DGI的位置。其余同上。
#注意：64位DGDecodeNV.dll只有一个，VS和AVS模式取决于LoadPlugin的模式。
#core.avs.LoadPlugin("C:/Program Files/dgdecnv/x64 Binaries/DGDecodeNV.dll")
#src = core.avs.DGSource("G:/DGNVindex/AAA/AAA.dgi",fieldop=2,deinterlace=0,crop_t=0,crop_b=0,crop_l=0,crop_r=0,resize_w=0,resize_h=0,fulldepth=True)

#源滤镜（FFMS2000）
#适用于WMV格式。写入源的平均帧率可转化把VFR转换为CFR。
#src = core.ffms2.Source(source="G:/DGNVindex/AAA/AAA.wmv",fpsnum=30000,fpsden=1001)

#截取
#0和1分别设置为起始帧和结束帧。
#src = core.std.Trim(src,0,1)

#反交错（QTGMC）
#src = haf.QTGMC(src, Preset='slower', TFF=True,opencl=False)

#反交错（DGNV）
#DGBob：硬件yadif反交错。order=1是TFF，0是BFF。mode=1是倍帧反交错，0是普通反交错。 PVBob：硬件PureVideo反交错。DGSource中反交错的独立版本。参数和上面一样。
#src = core.avs.DGBob(src,order=1,mode=1,device=255)
#src = core.avs.PVBob(src,order=1,mode=1,device=255)

#反胶卷过带（VS）
#order=0是底场优先，order=1是顶场优先。
"""
src = core.vivtc.VFM(src, order=1)
src = core.vivtc.VDecimate(src)
"""

#反胶卷过带（DGNV）
#参数参考DGNV说明档。
"""
src = core.avs.DGTelecide(src,mode=1, pthresh=3.5,dthresh=10.0,blend=False,map=False,show=False,device=255)
src = core.avs.DGDecimate(src,cycle=5,keep=4,device=255,show=False)                                                         
"""

#旋转90度
#先做矩阵转置，再左右或上下对称。若旋转效果错误，可以尝试把左右对称改为上下对称。
"""
src = core.std.Transpose(src)
src = core.std.FlipHorizontal(src)
#src = core.std.FlipVertical(src)
"""

#帧率改变（慎用）
#AVS的ChangeFPS改变帧率，只是单纯的增加重复帧或删除帧。增加帧率不会提高流畅度，降低帧率会严重降低流畅度，只建议用来微调帧率。
#src = haf.ChangeFPS(src, fpsnum=30000, fpsden=1001)
#AVS的AssumeFPS改变帧率。上面的是通过增加和减少帧来改变帧率，视频时长不变。这个是不动帧的数量，而是通过改变时长来调整帧率。
#src = core.std.AssumeFPS(src,fpsnum=30000, fpsden=1001)
#VFRtoCFR
#src = core.vfrtocfr.VFRToCFR(src, "G:/DGNVindex/AAA/AAA.tc2.txt", fpsnum=30000, fpsden=1001, drop=True)


#HDR to SDR(tonemap)
#Hable偏重保留细节，Mobius偏重色彩，二者选其一开启。Hable默认参数来自DOOM9论坛Selur的优化。Mobius默认参数是我自己优化的。
#各参数参考tonemap的GitHub说明。必须根据视频源调整参数，不能简单维持默认。参数包括nominal_luminance，exposure，Hable的abcdefw，Mobius的transition，peak。nominal_luminance是HDR视频的最大亮度。
#width=None, height=None可以调整为2560x1440,1920x1080,1280x720中任何一个。若不调整则不缩放。
"""
src = core.fmtc.bitdepth (src, bits=32,fulls=False,fulld=False)
fid = src.format.id
src = core.resize.Bilinear(src, format=vs.RGBS, range_in_s="limited", range_s="full", matrix_in_s="2020ncl", primaries_in_s="2020", primaries_s="2020", transfer_in_s="st2084", transfer_s="linear", chromaloc_in_s="center", chromaloc_s="center", dither_type="none", nominal_luminance=2000)
src = core.tonemap.Hable(src, exposure=20, a=0.22, b=0.3, c=0.1, d=0.2, e=0.01, f=0.3, w=11.2)
#src = core.tonemap.Mobius(src, exposure=6.8, transition=0.3, peak=300)
src = core.resize.Spline36(src, width=None, height=None, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="2020", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="center", chromaloc_s="center", dither_type="none")
src = core.fmtc.bitdepth (src, bits=10,fulls=False,fulld=False)
"""

#降噪（KNLMeansCL）
#对Y和UV平面降噪，一般来说只对Y降噪即可，选择性开启。h表示降噪力度。d和a表示时间和空间的降噪精度。, device_id是使用的GPU设备编号，0是第一个，1是第二个，以此类推。可以使用不同的GPU运算，如果有的话。
#src = core.knlm.KNLMeansCL(src, d=1,a=2,h=1.2,channels="Y", device_type='gpu', device_id=0)
#src = core.knlm.KNLMeansCL(src, d=1,a=2,h=1.2,channels="UV",device_type='gpu', device_id=0)

#降噪（SMDegrain）
##参数比较复杂，建议翻看AVS wiki。该参数只对亮度平面降噪。
#src = haf.SMDegrain(src,tr=2,thSAD=300,RefineMotion=True,contrasharp=True,chroma=True,plane=0,prefilter=4)

#SVP补帧
#在"num:60000,den:1001"处指定帧率。默认开启GPU运算。
"""
super_params="{gpu:1}"
analyse_params="{gpu:1}"
smoothfps_params="{rate:{num:60000,den:1001,abs:true},algo:23}"

super  = core.svp1.Super(src,super_params)
vectors = core.svp1.Analyse(super["clip"],super["data"],src,analyse_params)
smooth = core.svp2.SmoothFps(src,super["clip"],super["data"],vectors["clip"],vectors["data"],smoothfps_params)
src = core.std.AssumeFPS(smooth,fpsnum=smooth.fps_num,fpsden=smooth.fps_den)
"""

#DGNV处理滤镜（降噪和锐化）
#src = core.avs.DGDenoise(src,strength=0.15,blend=0.1,chroma=False,searchw=9,device=255)
#src = core.avs.DGSharpen(src,strength=1.0,device=255)

#Deblocking
#quant表示deblock强度。其他参数参考作者提供的说明。
#src = core.deblock.Deblock(src, quant=25, aoffset=0, boffset=0)

#Debanding
#range表示色带检测范围，y和cb cr表示三个平面色带的阈值。
#src = core.f3kdb.Deband(src,range=15,y=64,cb=64,cr=64,keep_tv_range=True,output_depth=8)

#黑边处理
#src = core.std.CropRel(src,left=0,right=0,top=0,bottom=0)
#src = core.std.AddBorders(src,left=0,right=0,top=0,bottom=0)

#字幕
#支持srt，ass，ssa等格式字幕文件。
#src = core.sub.TextFile(src,file="G:/DGNVindex/AAA/AAA1.ass")
#支持sup等图形字幕。
#src = core.sub.ImageFile(src,file="G:/DGNVindex//AAA/AAA1.sup")

#分辨率缩小（Spline36，非gamma-aware，锐度较高，有轻微ring）
#src = core.resize.Spline36(src,1280,720)

#分辨率缩小（Bilinear，非gamma-aware，锐度较低，无负面效应）
#src = core.resize.Bilinear(src,1280,720)

#分辨率调整或修改色彩标准（Spline36，gamma-aware）
#开启fmtc.resample可以做分辨率缩小。不建议用于放大。
#只能输入YUV流，不支持RGB流。
"""
src = core.fmtc.bitdepth (src, bits=32,fulls=False,fulld=False)
fid = src.format.id
src = core.resize.Bicubic(src, format=vs.RGBS, range_in_s="limited", range_s="full", matrix_in_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="709", transfer_s="linear", chromaloc_in_s="left", chromaloc_s="left", dither_type="none",filter_param_a=0,filter_param_b=0.5)
#src = core.fmtc.resample(src,1280,720,kernel="spline36",fulls=True,fulld=True,interlaced=0, interlacedd=0)
src = core.resize.Spline36(src, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="left", chromaloc_s="left", dither_type="none")
src = core.fmtc.bitdepth (src, bits=8,fulls=False,fulld=False)
"""

#分辨率缩小（Spline36，gamma-aware）
#如果不需要修改色彩空间，可以使用这个resize脚本。免去了YUVtoRGBtoYUV的重采样损失。
"""
src16 = core.fmtc.bitdepth (src, bits=16)
gray = core.std.ShufflePlanes(src16, 0, colorfamily=vs.GRAY)
gray = core.fmtc.transfer(gray,transs="709",transd="linear",fulls=False,fulld=False)
gray = core.fmtc.resample(gray,1280,720,kernel="spline36",interlaced=0, interlacedd=0)
gray = core.fmtc.transfer(gray,transs="linear",transd="709",fulls=False,fulld=False)
UV = core.fmtc.resample(src16,1280,720,kernel="spline36",interlaced=0, interlacedd=0)
down = core.std.ShufflePlanes([gray,UV],[0,1,2], vs.YUV)
src = core.fmtc.bitdepth (down, bits=8)
"""

#分辨率缩小（Spline36，gamma-aware，适用于光电转换标准为st2084或PQ的视频，使用X265压制时要输入HDR信息）
"""
src16 = core.fmtc.bitdepth (src, bits=16)                                                                                   
gray = core.std.ShufflePlanes(src16, 0, colorfamily=vs.GRAY)
gray = core.fmtc.transfer(gray,transs="2084",transd="linear",fulls=False,fulld=False)
gray = core.fmtc.resample(gray,1920,1080,kernel="spline36",cplace="MPEG1",cplaces="MPEG1",cplaced="MPEG1",interlaced=0, interlacedd=0)                                                                  
gray = core.fmtc.transfer(gray,transs="linear",transd="2084",fulls=False,fulld=False)
UV = core.fmtc.resample(src16,1920,1080,kernel="spline36",cplace="MPEG1",cplaces="MPEG1",cplaced="MPEG1",interlaced=0, interlacedd=0)                                                                   
down = core.std.ShufflePlanes([gray,UV],[0,1,2], vs.YUV)
src = core.fmtc.bitdepth (down, bits=10) 
""" 

#分辨率放大（Lanczos4+deringing，gamma-aware）
"""
src = core.fmtc.bitdepth (src, bits=16,fulls=False,fulld=False)
fid = src.format.id
src_rgb = core.resize.Bicubic(src, format=vs.RGB48, range_in_s="limited", range_s="full", matrix_in_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="709", transfer_s="linear", chromaloc_in_s="left", chromaloc_s="left", dither_type="none",filter_param_a=0,filter_param_b=0.5)
src_up1 = core.fmtc.resample(src_rgb,3840,2160,kernel="lanczos",taps=4,fulls=True,fulld=True,interlaced=0, interlacedd=0)
src_up2 = core.fmtc.resample(src_rgb,3840,2160, kernel="gauss",a1=100,fulls=True,fulld=True,interlaced=0, interlacedd=0)
src_up = core.rgvs.Repair(src_up1, src_up2,1)
src = core.resize.Spline36(src_up, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="left", chromaloc_s="left", dither_type="none")
src = core.fmtc.bitdepth (src, bits=8,fulls=False,fulld=False)
"""

#NNEDI3_resize16的分辨率放大（高质量，极慢，适合真人影片。需要import nnedi3_resample as nnrs）
#曲线和参数自行调整。去色带可以选择性开启。
"""
src = core.fmtc.bitdepth (src, bits=16)
src = nnrs.nnedi3_resample(src,target_width=1920,target_height=1080,curves="709",curved="709",mats="709", matd="709",sigmoid=True)
#src = core.f3kdb.Deband(src,range=15,y=64,cb=64,cr=64,keep_tv_range=True,output_depth=16)
src = core.fmtc.bitdepth (src, bits=8)
"""

#NNEDI3_resize16的分辨率放大（DVD-NTSC to 720P及以上）
#适合NTSC的480P DVD拉升到720P及以上分辨率，并将色彩标准转化为BT.709。修改分辨率后直接使用，别的参数一般来说不用动。使用之前记得先为隔行扫描视频做反交错或反胶卷过带。
#若觉得太慢可以尝试把32和RGBS修改为16和RGB48。
#核心是nnedi3_resample这行，若想换为waifu2x或普通的Lanczos4+deringing或其他算法，可以自行修改。核心思想就是先转化为 primary为709的线性RGB，做缩放，再转化为三个标准都为709的YUV。
"""
src = core.fmtc.bitdepth (src, bits=32,fulls=False,fulld=False)
fid = src.format.id
src = core.resize.Bicubic(src, format=vs.RGBS, range_in_s="limited", range_s="full", matrix_in_s="170m", primaries_in_s="170m", primaries_s="709", transfer_in_s="601", transfer_s="linear", chromaloc_in_s="left", chromaloc_s="left", dither_type="none",filter_param_a=0,filter_param_b=0.5)
src = nnrs.nnedi3_resample(src,target_width=1280,target_height=720,csp=vs.RGBS,curves="linear",curved="linear",mats="709",matd="709",fulls=True, fulld=True,cplaces="mpeg2",cplaced="mpeg2",sigmoid=True)
src = core.resize.Spline36(src, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="left", chromaloc_s="left", dither_type="none")
src = core.fmtc.bitdepth (src, bits=8,fulls=False,fulld=False)
"""

#Waifu2x-caffe的分辨率放大（高质量，极慢，适合动漫。需要将cudnn64_7.dll放置在VS插件文件夹中。）
#建议在处理前用SMD或KNL降噪，若不，Waifu2x的降噪等级要适当开启。
#scale表示放大的倍数，例如2是分辨率宽高都x2。processor是使用的GPU设备，例如0是第一个，1是第二个。其他参数参考Github说明。
#由于Waifu2x只能做2的倍数放大，所以在waifu2x后要用普通缩放滤镜缩放到指定分辨率。
"""
src = core.fmtc.bitdepth (src, bits=32,fulls=False,fulld=False)
fid = src.format.id
src = core.resize.Bicubic(src, format=vs.RGBS, range_in_s="limited", range_s="full", matrix_in_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="709", transfer_s="linear", chromaloc_in_s="left", chromaloc_s="left", dither_type="none",filter_param_a=0,filter_param_b=0.5)
src = core.caffe.Waifu2x(src, noise=-1, scale=2, block_w=128, block_h=128, model=3, cudnn=True, processor=0, tta=False)
src = core.fmtc.resample(src,1920,1080,kernel="spline36",fulls=True,fulld=True,interlaced=0, interlacedd=0)
src = core.resize.Spline36(src, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="left", chromaloc_s="left", dither_type="none")
src = core.fmtc.bitdepth (src, bits=8,fulls=False,fulld=False)
"""

#补偿性锐化
#AWarpSharp2锐化。一般不建议使用，除非源的锐利度实在太烂。depth表示锐化强度。
#src = core.warp.AWarpSharp2(src,depth=4,chroma=1)
#LSFmod锐化。另一种锐化，上面那个偏收线，适合动漫等线条明显的源。这个适合全部源。strength表示锐化强度。
#src = haf.LSFmod(src,strength=100,defaults='slow',kernel=19)

#位深改变
#不要反复拉升和降低位深！
#src = core.fmtc.bitdepth (src, bits=10)

src.set_output()

############################################################################################################################################################################################################################################################################################################
#说明：
#1.该VS模板作者为 零杀十一死，我的另一个ID是Morpheus。转载模板请勿移除此信息。
#2.该模板可以用于参考，也可以用于直接使用。但在使用前请熟悉VS的使用方法，使用时请随时学习滤镜的参数。
#3.有些脚本不适合所有视频，故需要了解该段脚本的适用范围再使用。
#4.（MOST important）正确的处理流程是：做部分处理（可选。例如截取，反交错，降噪等），再拉升到较高的bits，做部分处理（需要高精度处理的部分，例如缩放等），再dither到指定的bits输出。不要反复的拉升和降低bits，损失非常大。
#5.该模板可能存在一些错误。欢迎指出。

#changelog：
#r9(fixed):恢复import vapoursynth as vs写法。因为新写法无法使用vs.RGBS等format。
#r9：使用最新的from vapoursynth import core写法，与时俱进。一些其他修改。修复bug。
#r8：滤镜包更新至20180329。增加了源滤镜的相关信息和参数。将默认开启的源滤镜调整为L-SMASH。
#r7：增加了DVD分辨率拉升功能，缩放核心可以自己写，默认为nnedi3resample。完善waifu2x缩放。
#r6：滤镜包更新至20180326。增加了Waifu2x-caffe分辨率放大功能。
#r5：滤镜包更新至20180317。增加了旋转90°功能。
#r4：滤镜包更新到20180316。增加了VFRtoCFR滤镜。
#r3:恢复了之前的gamma-aware缩小的脚本。HDR缩放脚本中，为fmtc.resample增加了cplace="MPEG1"参数，因为HDR视频是中心对齐的。改了一下tonemap的默认参数（强调，依然只适用于我自己和我之前测试的视频）。fmtc.resample增加了interlaced=0, interlacedd=0参数，防止源滤镜错误识别扫描类型。
#r2:滤镜包更新到20180311。把HDR缩放分离成单独的脚本。
#r1：滤镜包更新到20180310。加入HDR转SDR的算法。修改模板的排版。将大量分辨率调整的脚本整合到一个脚本中，色彩更为准确，使用难度较高。