10 rem r0-c media fixture - sacrificial writable device 9 only.
20 rem this is a proof fixture, never a production save medium or recovery ux.
30 d=9:trap 9000
40 row=0:for k=0 to 1999:poke 2048+k,32:next k:t$="R0-C TWO-GENERATION MEDIA FIXTURE":gosub 9600
50 t$="SACRIFICIAL WRITABLE MEDIA ON DEVICE 9 ONLY":gosub 9600
60 t$="DEVICE 8 IS NOT USED OR PROBED.":gosub 9600
70 t$="I=INITIALIZE W=WRITE R=RECOVER C=CORRUPT F=FILL X=INTERRUPT Q=QUIT":gosub 9600
80 gosub 9700
90 if a=73 then gosub 1000:goto 40
100 if a=87 then gosub 2000:goto 40
110 if a=82 then gosub 5000:goto 40
120 if a=67 then gosub 6000:goto 40
130 if a=70 then gosub 7000:goto 40
140 if a=88 then gosub 8000:goto 40
150 if a=81 then end
160 t$="UNKNOWN ACTION - PRESS A KEY":gosub 9600:gosub 9700:goto 40
1000 rem initialize: retain two verified generations and select generation 2.
1010 t$="INITIALIZE WILL ERASE ONLY R0C FIXTURE FILES ON DEVICE 9.":gosub 9600
1020 t$="PRESS Y TO CONTINUE":gosub 9600:gosub 9700:if a<>89 then return
1030 gosub 9500:open 15,d,15,"S0:R0CG0":close 15:open 15,d,15,"S0:R0CG1":close 15:open 15,d,15,"S0:R0CSEL":close 15
1040 ns=0:ng=1:gosub 3000:gosub 4000:if ok=0 then return
1050 gosub 4500:if ok=0 then return
1060 ns=1:ng=2:gosub 3000:gosub 4000:if ok=0 then return
1070 gosub 4500:if ok=0 then return
1080 t$="INITIALIZE PASS: G0=1 AND G1=2 VERIFIED; SELECTOR=G1":gosub 9600:return
2000 rem normal transactional write: write, verify, then select inactive generation.
2010 gosub 5100:if sg<0 then t$="NO VALID SELECTOR - INITIALIZE OR RECOVER FIRST":gosub 9600:return
2020 ns=1-sg:ng=gg+1:t$="WRITING CANDIDATE GENERATION"+str$(ng)+" TO SLOT"+str$(ns):gosub 9600
2030 gosub 3000:gosub 4000:if ok=0 then t$="WRITE/VERIFY FAILED; PRIOR SELECTOR RETAINED":gosub 9600:return
2040 gosub 4500:if ok=0 then t$="SELECT FAILED; PRIOR SELECTOR RETAINED":gosub 9600:return
2050 t$="WRITE PASS: GENERATION"+str$(ng)+" COMMITTED AFTER VERIFY":gosub 9600:return
3000 rem write exactly one unselected generation file on device 9.
3010 if ns=0 then f$="R0CG0"
3020 if ns=1 then f$="R0CG1"
3030 gosub 9500:open 2,d,2,"@0:"+f$+",S,W"
3040 print#2,"R0CGEN";",";ng;",";ns;",";"R0C-FIXTURE"
3045 for n=1 to 512:print#2,"R0C-PAD";",";n:next n
3047 print#2,"R0C-END";",";"OK"
3050 close 2:gosub 9500:return
4000 rem verify the just-written generation before any selector write.
4010 ok=0:open 2,d,2,f$+",S,R":input#2,m$,rg,rs,p$
4020 if m$<>"R0CGEN" then return
4030 if rg<>ng then return
4040 if rs<>ns then return
4050 if p$<>"R0C-FIXTURE" then return
4060 for n=1 to 512:input#2,x$,xn:if x$<>"R0C-PAD" then close 2:return
4062 if xn<>n then close 2:return
4065 next n
4070 input#2,x$,c$:close 2
4080 if x$<>"R0C-END" then return
4090 if c$<>"OK" then return
4100 ok=1:t$="VERIFY PASS: SLOT"+str$(ns)+" GENERATION"+str$(ng):gosub 9600:return
4500 rem selector is written only after generation verification succeeds.
4510 ok=0:gosub 9500:open 2,d,2,"@0:R0CSEL,S,W"
4520 print#2,"R0CSEL";",";ns;",";ng;",";"COMMIT":close 2
4530 gosub 5100
4540 if sg<>ns then return
4550 if gg<>ng then return
4560 ok=1:t$="SELECTOR PASS: SLOT"+str$(sg)+" GENERATION"+str$(gg):gosub 9600:return
5000 rem recover from selector plus the two independently verified generations.
5010 gosub 5200:gosub 5300:gosub 5100
5020 if sg=0 and v0=gg then t$="RECOVERY PASS: SELECTOR CHOSE G0"+str$(gg):gosub 9600:return
5030 if sg=1 and v1=gg then t$="RECOVERY PASS: SELECTOR CHOSE G1"+str$(gg):gosub 9600:return
5040 if v0>=v1 and v0>=0 then t$="RECOVERY PASS: SELECTOR INVALID; HIGHEST VERIFIED G0"+str$(v0):gosub 9600:return
5050 if v1>v0 and v1>=0 then t$="RECOVERY PASS: SELECTOR INVALID; HIGHEST VERIFIED G1"+str$(v1):gosub 9600:return
5060 t$="RECOVERY FAIL: NO VERIFIED GENERATION":gosub 9600:return
5100 rem read selector; malformed or absent selector remains invalid.
5110 sg=-1:gg=-1:open 2,d,2,"R0CSEL,S,R":input#2,m$,sg,gg,c$:close 2
5120 if m$<>"R0CSEL" then sg=-1:gg=-1:return
5130 if c$<>"COMMIT" then sg=-1:gg=-1:return
5140 if sg<0 or sg>1 then sg=-1:gg=-1
5150 return
5200 rem read and validate generation 0.
5210 v0=-1:open 2,d,2,"R0CG0,S,R":input#2,m$,g0,s0,p$,c$:close 2
5220 if m$<>"R0CGEN" then return
5230 if s0<>0 then return
5240 if p$<>"R0C-FIXTURE" then return
5250 if c$<>"OK" then return
5260 v0=g0:return
5300 rem read and validate generation 1.
5310 v1=-1:open 2,d,2,"R0CG1,S,R":input#2,m$,g1,s1,p$,c$:close 2
5320 if m$<>"R0CGEN" then return
5330 if s1<>1 then return
5340 if p$<>"R0C-FIXTURE" then return
5350 if c$<>"OK" then return
5360 v1=g1:return
6000 rem intentionally corrupt only fixture selector or one fixture generation.
6010 t$="CORRUPT: S=SELECTOR, 0=GEN0, 1=GEN1 (DEVICE 9 ONLY)":gosub 9600
6020 gosub 9700:if a=83 then f$="R0CSEL"
6030 if a=48 then f$="R0CG0"
6040 if a=49 then f$="R0CG1"
6050 if a<>83 and a<>48 and a<>49 then return
6060 gosub 9500:open 2,d,2,"@0:"+f$+",S,W":print#2,"R0C-CORRUPT":close 2
6070 t$="CORRUPT WRITE COMPLETE. RUN R TO OBSERVE DETERMINISTIC RECOVERY.":gosub 9600:return
7000 rem fill only the sacrificial fixture image until the drive reports full.
7010 t$="FILL CONSUMES DEVICE 9. USE A FRESH SACRIFICIAL COPY.":gosub 9600
7020 t$="PRESS F TO CONTINUE":gosub 9600:gosub 9700:if a<>70 then return
7030 for n=1 to 4000:f$="R0CF"+str$(n):open 2,d,2,f$+",S,W":print#2,"FILL":close 2:next n
7040 t$="FILL LIMIT REACHED WITHOUT A DISK-FULL ERROR":gosub 9600:return
8000 rem interruption fixture: remove only while paused before selector commit.
8010 gosub 5100:if sg<0 then t$="NO VALID SELECTOR - INITIALIZE FIRST":gosub 9600:return
8020 ns=1-sg:ng=gg+1:gosub 3000:gosub 4000:if ok=0 then return
8030 t$="CANDIDATE VERIFIED; PRIOR SELECTOR IS STILL COMMITTED.":gosub 9600
8040 t$="SAFE TO REMOVE DEVICE 9 NOW: NO MEDIA I/O IS ACTIVE.":gosub 9600
8050 t$="REMOVE MEDIA, THEN PRESS C":gosub 9600:gosub 9700:if a<>67 then return
8060 t$="ATTEMPTING SELECTOR COMMIT; REMOVED MEDIA MUST FAIL SAFELY.":gosub 9600
8070 gosub 4500:return
9000 rem any device-9 BASIC/DOS fault returns without a successful claim.
9010 t$="MEDIA OPERATION FAILED ON DEVICE 9 - NO PASS CLAIM.":gosub 9600
9020 t$="REINSERT/REMOUNT SACRIFICIAL MEDIA BEFORE THE NEXT ACTION.":gosub 9600
9030 trap 0:goto 40
9500 rem all DOS status traffic is explicitly device 9.
9510 open 15,d,15:input#15,e,e$,t,s:close 15
9520 if e<>0 then t$="DOS STATUS"+str$(e)+e$:gosub 9600:return
9530 return
9600 col=0
9610 for k=1 to len(t$)
9620 z=asc(mid$(t$,k,1))
9630 if z>=193 and z<=218 then z=z-192
9640 poke 2048+row*80+col,z:col=col+1
9650 next k
9660 row=row+1:return
9700 rem normalize MEGA65 GET PETSCII/ASCII letter input to ASCII uppercase.
9710 get a$:if a$="" then goto 9710
9720 a=asc(a$):if a>=193 and a<=218 then a=a-128
9730 if a>=97 and a<=122 then a=a-32
9740 return
