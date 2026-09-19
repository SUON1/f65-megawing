package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.zip.CRC32;

/** Independent RH001 transport, retained-state and storage checker. */
public final class R0FResumeOracle {
    private R0FResumeOracle() { }
    private static void need(boolean ok,String what) {
        if(!ok)throw new IllegalArgumentException(what);
    }
    private static int word(byte[] b,int p){return (b[p]&255)|((b[p+1]&255)<<8);}
    private static long dword(byte[] b,int p){return word(b,p)|((long)word(b,p+2)<<16);}
    private static long crc(byte[] b){CRC32 c=new CRC32();c.update(b,0,252);return c.getValue();}
    private static int mix(int h,int v){return Integer.rotateLeft(h,5)^v;}
    // Independent array model of the existing non-gameplay 21-stage fixture.
    private static long golden(int ticks) {
        int[] x=new int[123],y=new int[123],z=new int[123],command=new int[9],next=new int[9];
        int[] table={3,7,2,11,5,13,1,9,4,15,6,12,8,14,10,0};int h=0;
        for(int i=0;i<123;i++){x[i]=i*17+3;y[i]=i*13+5;z[i]=i*7+257;}
        for(int tick=1;tick<=ticks;tick++){
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
    private static void validate(byte[] r,byte[] saved) {
        need(r.length==256&&saved.length==34,"length");
        need(Arrays.equals(Arrays.copyOf(r,5),new byte[]{'R','R','H','1',1}),"identity");
        need(r[5]==127&&r[6]==0&&r[7]==5,"completion/lockout");
        need(dword(r,252)==crc(r),"CRC");
        need(r[8]==1&&r[9]==5&&r[10]==0&&r[11]==1,"admission/storage sequence");
        need(r[12]==2&&r[13]==0x35&&r[14]==0&&r[15]==0,"canonical/ROM ownership");
        for(int p:new int[]{16,24,32,40})need(dword(r,p)!=0&&dword(r,p)==dword(r,p+4),"integrity pair "+p);
        need(word(r,48)==34&&word(r,50)==1&&dword(r,52)==golden(34),"same model continued at tick 34");
        need(r[56]==0&&r[57]==3&&r[58]==0&&r[59]==3,"default I/O before and after storage");
        for(int i=0;i<32;i++){
            need((r[64+i]&255)==(i^0x65),"input token");
            need((r[96+i]&255)==(((golden(33)>>>((i&3)*8))^i)&255),"saved application payload");
            need(r[128+i]==r[96+i]&&saved[2+i]==r[96+i],"readback/extracted SAVE");
        }
        need(word(r,160)==word(r,164)+32&&word(r,162)==word(r,164)+32,"LOAD lengths");
        need(word(saved,0)==word(r,166),"SAVE load header");
        CRC32 dos=new CRC32(),reclaimed=new CRC32();
        for(int i=0;i<8192;i++)dos.update((i^(i>>>8)^0x93)&255);
        for(int i=0;i<131072;i++)reclaimed.update((i^0x5a)&255);
        need(dword(r,168)==dos.getValue()&&dword(r,172)==dos.getValue(),"DOS-overlay state preservation");
        need(dword(r,176)==reclaimed.getValue(),"ROM stores actually overwritten");
    }
    public static void main(String[] args)throws Exception {
        need(golden(33)==0xd9eeab81L,"baseline independent fixture");
        if(args.length==1&&args[0].equals("--model")){
            System.out.printf("RH001 independent continuation golden: %08X -> %08X%n",golden(33),golden(34));return;
        }
        need(args.length==2,"usage: result.bin saved.prg OR --model");
        byte[] r=Files.readAllBytes(Path.of(args[0])),saved=Files.readAllBytes(Path.of(args[1]));
        validate(r,saved);int rejected=0;
        for(int p:new int[]{0,4,5,6,7,8,9,10,11,12,13,14,15,16,24,32,40,48,50,52,56,57,58,59,64,96,128,160,162,164,166,168,172,176}){
            byte[] bad=r.clone();bad[p]^=64;long c=crc(bad);
            for(int i=0;i<4;i++)bad[252+i]=(byte)(c>>>(8*i));
            boolean failed=false;
            try{validate(bad,saved);}catch(IllegalArgumentException ex){failed=true;}
            need(failed,"accepted resealed corruption "+p);rejected++;
        }
        for(int p=0;p<saved.length;p++){
            byte[] bad=saved.clone();bad[p]^=1;boolean failed=false;
            try{validate(r,bad);}catch(IllegalArgumentException ex){failed=true;}
            need(failed,"accepted saved corruption "+p);rejected++;
        }
        System.out.printf("RH001 same-run/ROM/state/LOAD/SAVE/readback PASS; %d corruptions rejected.%n",rejected);
        System.out.println("Isolated returning-handoff evidence only; not full R0-F or physical acceptance.");
    }
}
