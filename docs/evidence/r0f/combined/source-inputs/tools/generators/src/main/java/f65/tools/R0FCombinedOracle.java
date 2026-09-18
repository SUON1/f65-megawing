package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.zip.CRC32;
import java.util.regex.Pattern;
import java.util.regex.Matcher;

/** Independent CF001 fixture model and raw-count reducer. No SI promotion. */
public final class R0FCombinedOracle {
    private R0FCombinedOracle() { }
    private static void require(boolean value, String what) {
        if (!value) throw new IllegalArgumentException(what);
    }
    private static int u16(byte[] b,int at) { return (b[at]&255)|((b[at+1]&255)<<8); }
    private static long u32(byte[] b,int at) { return u16(b,at)|((long)u16(b,at+2)<<16); }
    private static long crc(byte[] b,int n) { CRC32 c=new CRC32();c.update(b,0,n);return c.getValue(); }
    private static int mix(int h,int v) { return Integer.rotateLeft(h,5)^v; }
    private static long golden() {
        int[] x=new int[123],y=new int[123],z=new int[123],command=new int[9],next=new int[9];
        int[] table={3,7,2,11,5,13,1,9,4,15,6,12,8,14,10,0};int h=0;
        for(int i=0;i<123;i++){x[i]=i*17+3;y[i]=i*13+5;z[i]=i*7+257;}
        for(int tick=1;tick<=33;tick++){
            System.arraycopy(next,0,command,0,9);
            int environment=(tick&7)+table[tick&15];
            for(int stage=5;stage<=10;stage++)for(int i=0;i<9;i++){
                int v=(x[i]+command[i]+environment+stage)&65535;
                x[i]=v^(y[i]>>>3);y[i]=(y[i]+table[v&15])&65535;z[i]=257+((z[i]+i+stage)&1023);
            }
            for(int i=9;i<97;i++){x[i]=(x[i]+table[(i+tick)&15])&65535;y[i]^=x[i]>>>2;z[i]=257+((z[i]+3)&1023);}
            for(int i=0;i<9;i++)y[i]=(y[i]+(i==0?8:7))&65535;
            for(int i=113;i<123;i++){x[i]=(x[i]+x[(i-113)%9])&65535;y[i]^=tick;}
            for(int i=0;i<9;i++)next[i]=(x[113+i]^tick)&15;
            for(int i=97;i<113;i++)x[i]=(x[i]+environment+1)&65535;
            h=mix(0x0065cf01,tick);
            for(int i=0;i<123;i++){h=mix(h,x[i]);h=mix(h,y[i]);h=mix(h,z[i]);}
            for(int i=0;i<9;i++){h=mix(h,command[i]);h=mix(h,next[i]);}
        }
        return Integer.toUnsignedLong(h);
    }
    private static void validate(byte[] r,byte[] raw) {
        require(r.length==1792&&raw.length==5280,"length");
        require(r[0]=='R'&&r[1]=='C'&&r[2]=='F'&&r[3]=='1'&&r[4]==1,"identity");
        require(r[5]==127&&r[6]==0,"acquisition incomplete/fault");
        require(u32(r,1788)==crc(r,1788)&&u32(r,72)==crc(raw,5280),"CRC");
        require(r[7]==1||r[7]==2,"reference class");
        require(r[10]==2&&(r[11]&255)==0x35&&r[12]==2&&r[13]==0,"canonical/recovery");
        require(u32(r,16)==u32(r,20)&&u32(r,152)==131072,"ROM bytes restored");
        require(u32(r,24)==u32(r,28),"reserve changed");
        require(u16(r,68)==0x300&&u16(r,70)==5280,"capture location/length");
        require(u32(r,164)==2640&&u16(r,168)==187,"executed population/ticks");
        require(u32(r,144)==golden(),"independent authority checksum");
        require(u16(r,124)==1&&r[120]==3&&r[121]==64&&(r[122]&255)==16,"fault/snapshot/queue evidence");
        require((r[148]&255)==15&&u32(r,92)==32&&u32(r,1672)==32,"tiers/scripted edges consumed once");
        require(u32(r,1668)<=u32(r,88),"consumed nonexistent real edges");
        require(u16(r,76)>0&&u16(r,78)>32&&u32(r,84)>=1000&&u32(r,96)>=1000,"display-rate services absent");
        require(u32(r,100)>0&&u32(r,104)>0&&u32(r,108)>0&&u32(r,112)>0,"PCM/preemption/render/swap absent");
        require(u16(r,126)>0&&u16(r,126)<256&&u16(r,128)<4096,"stack bounds");
        long before=0,after=0;for(int i=0;i<16;i++){before+=u32(r,176+4*i);after+=u32(r,1536+4*i);}
        require(u32(r,32)==before/16&&u32(r,136)==after/16&&u16(r,172)==16,"frame reduction");
        long clocks=u32(r,36),counts=u32(r,32);
        require(counts>0&&clocks>0&&u32(r,40)==405000L*counts*65536/clocks,"period rational");
        if(r[7]==1)require(clocks==((r[8]&128)!=0?676962:808704),"pinned Xemu profile");
        require(u32(r,64)==Math.abs(u32(r,60)-530000),"calibration residual");
        for(int cohort=0;cohort<80;cohort++){
            int[] d=new int[33];long sum=0;
            for(int i=0;i<33;i++){d[i]=u16(raw,(cohort*33+i)*2);require(d[i]>0,"zero duration");sum+=d[i];}
            Arrays.sort(d);int at=256+cohort*16;
            require(u16(r,at)==d[16]&&u16(r,at+2)==d[31]&&u16(r,at+4)==d[32],"percentiles cohort "+cohort);
            require(u32(r,at+8)==sum&&u32(r,at+12)>=sum,"window sum/span");
        }
        long swaps=0;for(int i=0;i<80;i++)swaps+=r[1676+i]&255;
        require(swaps==u32(r,112),"per-phase swaps sum");
    }
    private static void reseal(byte[] r){long c=crc(r,1788);for(int i=0;i<4;i++)r[1788+i]=(byte)(c>>>(8*i));}
    private static byte[] pages(String[] paths)throws Exception {
        require(paths.length==14,"all fourteen pages required");
        byte[] stream=new byte[7072];boolean[] seen=new boolean[14];long resultCrc=-1,rawCrc=-1;
        Pattern header=Pattern.compile("^([0-9A-F]{2})\\s+([0-9A-F]{4})\\s+([0-9A-F]{4})\\s+([0-9A-F]{8})\\s+([0-9A-F]{8})\\s*$");
        for(String path:paths){int page=-1,offset=0,amount=0;StringBuilder hex=new StringBuilder();
            for(String line:Files.readAllLines(Path.of(path))){String clean=line.strip().toUpperCase(java.util.Locale.ROOT);Matcher m=header.matcher(clean);
                if(m.matches()){require(page==-1,"duplicate header");page=Integer.parseInt(m.group(1),16)-1;offset=Integer.parseInt(m.group(2),16);amount=Integer.parseInt(m.group(3),16);
                    long a=Long.parseLong(m.group(4),16),b=Long.parseLong(m.group(5),16);
                    if(resultCrc==-1){resultCrc=a;rawCrc=b;}require(resultCrc==a&&rawCrc==b,"mixed acquisition headers");}
                else if(clean.matches("[0-9A-F]{64}"))hex.append(clean);
            }
            require(page>=0&&page<14&&!seen[page],"missing/duplicate/out-of-range page");seen[page]=true;
            require(offset==page*512&&amount==(page==13?416:512)&&hex.length()==1024,"page offset/length/rows");
            byte[] bytes=java.util.HexFormat.of().parseHex(hex);System.arraycopy(bytes,0,stream,offset,amount);
            for(int i=amount;i<512;i++)require(bytes[i]==0,"nonzero last-page padding");
        }
        require(u32(stream,1788)==resultCrc&&u32(stream,72)==rawCrc,"page header CRC mismatch");return stream;
    }
    public static void main(String[] args)throws Exception {
        require(golden()==0xd9eeab81L,"host golden fixture");
        if(args.length==1&&args[0].equals("--model")){System.out.printf("Independent Java CF001 33-tick golden PASS: %08X%n",golden());return;}
        byte[] r,raw;
        if(args.length>0&&args[0].equals("--pages")){byte[] stream=pages(Arrays.copyOfRange(args,1,args.length));r=Arrays.copyOf(stream,1792);raw=Arrays.copyOfRange(stream,1792,7072);}
        else {require(args.length==2,"usage: --model OR result.bin durations.bin OR --pages fourteen-text-files");r=Files.readAllBytes(Path.of(args[0]));raw=Files.readAllBytes(Path.of(args[1]));}
        validate(r,raw);
        int rejected=0;
        for(int at:new int[]{0,4,5,6,7,10,11,12,13,16,24,68,70,72,120,121,122,124,144,148,152,164,168,172,256,258,260,264,1672,1676}){
            byte[] bad=r.clone();bad[at]^=64;reseal(bad);boolean failed=false;
            try{validate(bad,raw);}catch(IllegalArgumentException ex){failed=true;}
            require(failed,"mutation accepted "+at);rejected++;
        }
        System.out.printf("CF001 acquisition/oracle PASS: 2640 samples, 80 windows, golden %08X, %d resealed mutations rejected.%n",golden(),rejected);
        System.out.println("Reference="+(r[7]==1?"XEMU MODEL ONLY":"NOMINAL HARDWARE COUNTER RATIO")+"; no traceable SI/external latency/R0-F acceptance.");
        String[] cases={"NORMAL","LAG","TIERS","FAULT","PRESSURE"};
        for(int kind=0;kind<5;kind++){
            long swaps=0,span=0,max=0,late=0;for(int i=0;i<16;i++){
                int at=256+(kind*16+i)*16;span+=u32(r,at+12);swaps+=r[1676+kind*16+i]&255;
                max=Math.max(max,u16(r,at+4));late=Math.max(late,u16(r,at+6));}
            double seconds=(double)span*u32(r,36)/u32(r,32)/40500000;
            System.out.printf("%s: %d swaps / %.6f nominal s = %.3f Hz; max tick=%d CIA; max late=%d CIA%n",cases[kind],swaps,seconds,swaps/seconds,max,late);
        }
        System.out.printf("Overhead=%d CIA; calibration=%d nominal CPU clocks, residual=%d; DMA max=%d CIA; service gap=%d CIA; stacks hardware/software=%d/%d bytes%n",u32(r,44),u32(r,60),u32(r,64),u32(r,80),u32(r,132),u16(r,126),u16(r,128));
    }
}
