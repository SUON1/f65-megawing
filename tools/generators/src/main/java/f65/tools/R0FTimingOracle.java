package f65.tools;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

/** Independent raw-capture reduction; no target-generated expected values. */
public final class R0FTimingOracle {
    static int u16(byte[] b, int p) { return (b[p] & 255) | (b[p+1] & 255) << 8; }
    static long u32(byte[] b, int p) { return Integer.toUnsignedLong(u16(b,p) | u16(b,p+2) << 16); }
    static void require(boolean ok, String message) { if (!ok) throw new IllegalArgumentException(message); }
    static void validate(byte[] b) {
        require(b.length == 11136, "result/raw length");
        require(Arrays.equals(Arrays.copyOf(b, 7), new byte[]{'R','0','F','1',2,100,21}), "identity");
        int sum = 0;
        for (int i=0;i<255;i++) sum += b[i]&255;
        require((sum&255)==(b[255]&255), "checksum");
        require(b[7]==127 && b[151]==127 && b[252]==0 && b[254]==0, "status");
        require(u16(b,250)==10880 && u32(b,244)==10000, "metadata");
        require(Arrays.equals(Arrays.copyOfRange(b,144,151),new byte[]{'C','T',1,16,33,5,16}),"timing header");
        require(u16(b,156)==16 && (b[253]&255)==3,"frame/snapshot metadata");
        require(u16(b,248)>=0x2001 && u16(b,248)<=0xd000-10880,"raw pointer range");
        for(int p:new int[]{152,240}) require(u32(b,p)>=128000 && u32(b,p)<=960000,"frame count guard");
        int[] profile={9,16,24,48,64};
        for(int i=0;i<profile.length;i++) require(u32(b,8+i*4)==profile[i],"profile");
        require(Arrays.equals(Arrays.copyOfRange(b,28,33),new byte[]{3,64,1,0,5}),"snapshot metadata");
        for(int i=33;i<40;i++) require(b[i]==0,"reserved header");
        for(int i=60;i<64;i++) require(b[i]==0,"reserved functional");
        int hash = 0x0065e001;
        for(int t=1;t<=1000;t++) hash = hash<<5 ^ hash>>>2 ^ t;
        for(int c=0;c<5;c++) {
            require(u32(b,40+c*4)==Integer.toUnsignedLong(hash), "functional checksum");
            int at=64+c*16;
            require(b[at]==c && b[at+1]==1 && u16(b,at+2)==1000, "case identity/count");
            require(u16(b,at+4)==(c==1?202:1000) && u16(b,at+6)==(c==1?798:0), "snapshot counts");
            require(u16(b,at+8)==(c==4?2000:1000) && u16(b,at+10)==(c==4?2000:1000), "proxy services");
            require(b[at+12]==(c==2?63:0) && b[at+13]==(c==3?1:0), "fault/shedding");
            require(b[at+14]==0 && b[at+15]==0,"reserved case");
            int[] duration = new int[528];
            int misses=0, late=0;
            for(int i=0;i<528;i++) {
                int p=256+(c*528+i)*4;
                duration[i]=u16(b,p);
                int v=u16(b,p+2);
                if(v!=0) misses++;
                late=Math.max(late,v);
            }
            Arrays.sort(duration);
            at=160+c*16;
            require(u16(b,at)==duration[263], "p50");
            require(u16(b,at+2)==duration[501], "p95");
            require(u16(b,at+4)==duration[527] && duration[527]>0, "max/nonstalled clock");
            require(u16(b,at+6)==late && u16(b,at+8)==misses, "lateness/misses");
            require(u16(b,at+10)==65535, "phase mask");
            long maxSpan=0;
            for(int phase=0;phase<16;phase++) {
                long span=u32(b,256+5*528*4+(c*16+phase)*4);
                require(span>=320000 && span<=395535, "33-tick cohort extent");
                maxSpan=Math.max(maxSpan,span);
            }
            require(u32(b,at+12)==maxSpan, "cohort maximum");
        }
    }
    public static void main(String[] args) throws Exception {
        byte[] original=Files.readAllBytes(Path.of(args[0]));
        validate(original);
        int rejected=0;
        // Corrupt summary values with a recomputed checksum: reduction must
        // still reject them. Exercise each case and each summary field.
        for(int c=0;c<5;c++) for(int offset:new int[]{0,2,4,6,8,10,12}) {
            byte[] bad=original.clone(); bad[160+c*16+offset]^=1;
            int sum=0; for(int i=0;i<255;i++) sum+=bad[i]&255; bad[255]=(byte)sum;
            try { validate(bad); } catch(IllegalArgumentException expected) { rejected++; continue; }
            throw new IllegalStateException("accepted summary corruption");
        }
        int fields=0;
        for(int offset=0;offset<255;offset++) {
            if(!(offset<152 || offset==156 || offset==157 || offset>=244 && offset<=247 || offset>=250)) continue;
            byte[] bad=original.clone(); bad[offset]^=1;
            int sum=0; for(int i=0;i<255;i++) sum+=bad[i]&255; bad[255]=(byte)sum;
            try { validate(bad); } catch(IllegalArgumentException expected) { fields++; continue; }
            throw new IllegalStateException("accepted fixed-field corruption at "+offset);
        }
        System.out.println("PASS: 2640 raw samples, 80 cohort spans, functional oracle; " + rejected + " summary and "+fields+" fixed-field corruptions rejected");
    }
}
