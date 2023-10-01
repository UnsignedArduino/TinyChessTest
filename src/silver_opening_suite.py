import gzip
import logging
from base64 import b85decode

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def get_silver_opening_suite_pgn() -> str:
    logger.debug(f"Decompressing Silver opening suite")
    return gzip.decompress(
        b85decode(
            b"ABzY8QPLP?0{_LDTW{OO635^5DHeVyklKVKUiEZf%5G7lQ7oxIffnasxg3!^rpbV!93`K=GqX#@cD>2N;mSdxTjJRB+nN7dcK*J7gr*l47yq67y{&rCuWls0`Vao{_&0sFX%9_~AJXeTOa7<Zs(yq{Y!CR3K2B???!`q~b@@+w@$nNhRa5ZS!v0X>cX>x|ZkHd$#r4!b{YSTTD=wy||KQu(>!xXY*|(kf`PxIL%ul$12ie{8>&eX91tJf{+*|E@vD!t#_cC9+o8b2v-?|O-)sJioN3?CQY3>!iD9E<7n2WTCMc{qB`Y7m6=;gl1BUdKhHbq_S%S&;+|MKtveOD=q<@3dema9MjpQ;*8m073=Eias%@A?4Hp!@#T<dtkLMG1KUWotWYe>$$k`l!id7%WzyHaLs$p!x8#SVVmIDa0c7@<6C#9!wH%jZfqV3vZLpgp9;&N};gI@>tAfUYgC>UuJU;0#^W2Xzp9_t9;0+-U2O5Mue6R(2yRY@;#J-jF71#K1qU>9q|ccCt|QEy>n-L+f<k0Lz_d_Sj>-o$L0ft2>Z|x--Sp5pK`Jvj~zM0>{qBE=rSp2pIER%Il^*t=oRY6@2r}g%q?J&cw8{MP|K!P4+@=v$!Oyd%pjl<(aRYOQd>iUU=W#G8r!~Y;Ipi23ysCpH4XL?#mO_&QWFir!Z0#o5xc^$RT4F}k&mdeuOmpOvk?)1sS-FS*7V@(<CdfrCXSwPNRdpsbLIutHQbj~1K$^mbkt%32C=}zx?%u2Ukou3P=*0^jHd~v#J?*;j0s9mnKSXct2%Y5e-;~zWMqFJ7Utx&GrSOpK^+Z^B5-T_^<j_Im28CUd;Hi&VR04;SXFBXghN9}b7yteQg-dtd)Z*gb)7%TMuElp*?e5<m9d_~0po%~Ub_H9#sl1&d?%as(PnVq(qPg-t`CBt{0xWkGhzzvjbGMszps?6Z2%Sy0g$cv5kJK<rzbjoBv6n75P~ugrKy-ED=ecEuS6dyV=R~`8qy;^V3oZ-x(khMrK*~n5v=lT(l{SGEJFTnPrPKUz2sS<Bt?vdlo69iPN+dkOv)fg;B$9EkocKW3icwLdEND_-<U1yb`QCYTIhfpH>`@Zv@lXSwCqEp9+9}h8I0dP!oF;(d#kwkz6$`m0f1>uIk@s?@)DA~<XNc8?z9LelKf^Red^v89+fBTDpM~#;+OFQ`i(k6n0-KPQeVG_v}$aQ<0t3jRuDEL&$@}#)L=d#w{i~TP9Ew#*h<tOa>N2&b0IajkUT^DY${du&|Pih;VX0&`y*HO=id#XmF`lCP;2ixpX(4p5yoPzjEwj?XLQraqP6)(ym%8foVv++3Xj;s+)Ydpg2dbwy1UC+Uo<dk19?W~i_K0YG$g~^ze1s!`QH0%<{soq{x5I49c2d+NDI+q`X)qWH2hpt3}yZ#1#&iK3{(vfTKD-(mGH<@B&!-F!Q1h9RtOQ6gc7|TuMw%WawgWlbkNXL>ATI-ayoLA2rrr^o>d!d(iP%5BQTiNRp8q6KV;X*y((?ChYoFDk+AHj)}ztNE~i>g@$6oA%>=};`F~c8{A^27%dwj%c-cgyS)i>~)IdpUjg<d0nx7rXA$XAFu%EmuQ6f-2f7**1*g><mg+MU!Oc7q{1H7sask=ey9rRth+x^Jyxg)#H*ysr1w^1Uu(xLGWr*osNYI|$Q2cavQ)hmacvgfnTbDd6ZU${H=-+EbFN9W5haB4c2PptO2Z@gTY))sXj%_s@Vz+sKPIeZbnx1ZqarMNw+Qes6Q9;HqFqQor?ebb1I{t@5jN6vnOcSQPHmL4Xt_7qpK@JTj&QLkqn;!0e18cn^o43n4fxyZ;t4XGT;SQW6;CLeN5gSIs+)+h6~u%6X1A_vK+nnn&2l*z=)NkgfwUbq}{{L4xHl2yM4%Y<mTcoRgFE+cOPvnPnC-%!3Or)j{Lar=fCH<0j5F>}|0EZe#UvH!B~;o)^sH;(pxPUW?4E^K{WVmVBz!xD_%;=s16mKOK8nT@>5!B@13hxGmlLSV-9ii!%UhxCyF5|ii#6DmIw9bL5Tawagk<*<|=H-6xT4Gi~my4|9=yxH^^;wl<0`f0Q}H?8Qf?XcjX(J++fgjDiu)#144UmgVy)fKrF>dy!0Y-P+%@M0z8Il&Q~i!b}Y>`Lj1mHo}QS4R5G7d~0+c30*(DUpM!s|IrRwO-!0))w#P<yzG^tWM6RS&{3IJ25PMD@-8yjw~$$;ch+P*X{t#4r)a43)a1=guZVrDB^HT6sHBN!d&X;^-H?d(d(Do{*fecEUxImT!v+QsiB+>08U^mFp}6EjFrA344zmX@|p=X{igTVGg#~xCW@kH1*aLTaUnf}b$8Q@jS>wHua$yNz3ndWb{aUrblT(0%^s&oW8^)qwh-H*z0wP;7F%cEAA-#Pe`_%x|4cE071^5QqHr1m&)0TsR)=m+I5Vrssopv@5F&=4H>oHY^Zj_L<Hiw<RrT<7@BrGVTC2GQi9dIU<TMq;?{Ady$y{(v+K>&mza>*C1CwBP=fkr(WL1M@ePwf-ar3H;k<mh3*K;y4%ipoCYE?8z27CyJmDLfS_f=CoS%Lpiw!M9M0XlYq(do800Yc@>hxH_`*L1Q4$}a8}+h0)GN-SZmw+**Ra1JJVdoT39ZRmlP+1OhZU@nB|W^R)uv{a#H)PJ7`&=1zSZWoJl5_+=4NSAca!-`55zQkO?Osw>+@Cw6lr>}&~-Og-IoOc0T2xDAgA^h$i?@P*rKs5jW"
        )
    ).decode()
