import vapoursynth as vs
import sys

#CPU线程数
core = vs.get_core(accept_lowercase=True,threads=8)

#该脚本使用的最大内存（MB）
core.max_cache_size = 12000

#构建如下的目录结构，把图片放在里面，可以批量处理。%d从1开始。滤镜参数自行学习，下同。该脚本不支持有alpha通道的图片。
src = core.imwri.Read("G:/DGNVindex/AAA/src/AAA_%d.jpg",firstnum=1,mismatch=True,alpha=False,float_output=False)

#黑边处理。可以不是黑色的，自行加参数调整。
#src = core.std.CropRel(src,left=0,right=0,top=0,bottom=0)
#src = core.std.AddBorders(src,left=0,right=0,top=0,bottom=0)

#waifu2x
#waifu2x只能做2/4/8...倍放大，故把原图拉升到略大于指定分辨率，再用spline36缩到指定分辨率即可。
#model=3适合处理动漫类图片。4适合处理照片类图片。其他参数参考作者说明。
src = core.fmtc.bitdepth (src, bits=32,fulls=True,fulld=True)
src = core.caffe.Waifu2x(src, noise=0, scale=2, block_w=192, block_h=108, model=4, cudnn=True, processor=0, tta=True)
src = core.fmtc.resample(src,2560,1440,kernel="spline36",fulls=True,fulld=True,interlaced=0, interlacedd=0)
src = core.fmtc.bitdepth (src, bits=8,fulls=True,fulld=True)

#nnedi3_resample
"""
src = core.fmtc.bitdepth (src, bits=32,fulls=True,fulld=True)
src = nnrs.nnedi3_resample(src,target_width=2560,target_height=1440,csp=vs.RGBS,curves="srgb",curved="srgb",fulls=True, fulld=True,sigmoid=True)
src = core.fmtc.bitdepth (src, bits=8,fulls=True,fulld=True)
"""

#将结果写入 output/ 下。需要提前建立output文件夹。
output = core.imwri.Write(clip=src,imgformat="PNG",filename="G:/DGNVindex/AAA/output/AAA_waifu2x_%d.png",firstnum=1,quality=100,dither=False,compression_type=None,overwrite=True,alpha=None)

#输出。按F7进入benchmark模式，跑分结束即处理完成。
output.set_output()