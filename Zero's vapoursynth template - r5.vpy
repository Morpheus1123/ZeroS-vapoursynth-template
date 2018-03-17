import vapoursynth as vs
import sys
import havsfunc as haf
import mvsfunc as mvf
#import adjust
#import avsfunc
#import finedehalo
#import finesharp
#import hysteria
#import MCDenoise
#import muvsfunc as muf
#import nnedi3_resample as nnrs
#import vsTAAmbk
#import xvsfunc as xvf

#指定CPU线程数
core = vs.get_core(accept_lowercase=True,threads=8)

#指定VS使用的最大内存（MB）
core.max_cache_size = 12000

#注意：一个完整的处理过程应该是先拉升到高位深，做处理，最后统一缩回指定位深。不要反复拉升和降低位深。
#r5：滤镜包更新至20180317。增加了旋转90°功能。
#r4：滤镜包更新到20180316。增加了VFRtoCFR滤镜。
#r3:恢复了之前的gamma-aware缩小的脚本。HDR缩放脚本中，为fmtc.resample增加了cplace="MPEG1"参数，因为HDR视频是中心对齐的。改了一下tonemap的默认参数（强调，依然只适用于我自己和我之前测试的视频）。fmtc.resample增加了interlaced=0, interlacedd=0参数，防止源滤镜错误识别扫描类型。
#r2:滤镜包更新到20180311。把HDR缩放分离成单独的脚本。
#r1：滤镜包更新到20180310。加入HDR转SDR的算法。修改模板的排版。将大量分辨率调整的脚本整合到一个脚本中，色彩更为准确，使用难度较高。

#源滤镜（DGNV）
#选择64位DGDecodeNV.dll和DGI的位置。fieldop=0表示遵循Pulldown Flags，1是强制pulldown，2是什么都不做。deinterlace=0为不反交错，1为普通反交错，2为倍帧反交错。可以使用DGNV内置的缩放滤镜，速度非常快，质量一般。
core.avs.LoadPlugin("C:/Program Files/dgdecnv/x64 Binaries/DGDecodeNV.dll")
src = core.avs.DGSource("G:/DGNVindex/AAA/AAA.dgi",fieldop=2,deinterlace=0)
#src = core.avs.DGSource("G:/DGNVindex/AAA/AAA.dgi",fieldop=2,deinterlace=0,resize_w=1280, resize_h=720)

#源滤镜（L-SMASH）
#LibavSMASHSource适用于MP4格式，不需要做索引，可以快速打开。LWLibavSource适用于其他格式，需要等待制作索引。
#src = core.lsmas.LibavSMASHSource(source="G:/DGNVindex/AAA/AAA.mp4")
#src = core.lsmas.LWLibavSource(source="G:/DGNVindex/AAA/AAA.mkv")

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
super_params="{pel:2,gpu:1}"
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
#src = core.fmtc.resample(src,1280,720,kernel="spline36",fulls=True,fulld=True)
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
src_up1 = core.fmtc.resample(src_rgb,3840,2160,kernel="lanczos",taps=4,fulls=True,fulld=True)
src_up2 = core.fmtc.resample(src_rgb,3840,2160, kernel="gauss",a1=100,fulls=True,fulld=True)
src_up = core.rgvs.Repair(src_up1, src_up2,1)
src = core.resize.Spline36(src_up, format=fid, range_in_s="full", range_s="limited", matrix_s="709", primaries_in_s="709", primaries_s="709", transfer_in_s="linear", transfer_s="709", chromaloc_in_s="left", chromaloc_s="left", dither_type="none")
src = core.fmtc.bitdepth (src, bits=8,fulls=False,fulld=False)
"""

#NNEDI3_resize16的分辨率放大（高质量，极慢，需要import nnedi3_resample as nnrs）
#曲线和参数自行调整。去色带可以选择性开启。
"""
src = core.fmtc.bitdepth (src, bits=16)
src = nnrs.nnedi3_resample(src,target_width=1920,target_height=1080,curves="709",curved="709",mats="709", matd="709",sigmoid=True)
#src = core.f3kdb.Deband(src,range=15,y=64,cb=64,cr=64,keep_tv_range=True,output_depth=16)
src = core.fmtc.bitdepth (src, bits=8)
"""

#补偿性锐化
#AWarpSharp2锐化。一般不建议使用，除非源的锐利度实在太烂。depth表示锐化强度。
#src = core.warp.AWarpSharp2(src,depth=4,chroma=1)
#LSFmod锐化。另一种锐化，上面那个偏收线，适合动漫等线条明显的源。这个适合全部源。strength表示锐化强度。
#src = haf.LSFmod(src,strength=100,defaults='slow',kernel=19)

#位深改变
#切忌不要反复拉升和降低位深！
#src = core.fmtc.bitdepth (src, bits=10)

src.set_output()
