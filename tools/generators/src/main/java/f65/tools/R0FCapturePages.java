package f65.tools;

import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Locale;
import java.util.zip.CRC32;

/** Independent decoder of the private F5 screen transport; never an OCR repairer. */
public final class R0FCapturePages {
    static final int TOTAL=11136, PAGE=512, COUNT=22, SCREEN=2000;
    static void require(boolean value, String why) { if (!value) throw new IllegalArgumentException(why); }
    static String fmt(String format, Object... args) { return String.format(Locale.ROOT,format,args); }
    static long crc(byte[] b) { CRC32 c=new CRC32(); c.update(b); return c.getValue(); }
    static String row(String screen,int row) { return screen.substring(row*80,(row+1)*80).stripTrailing(); }
    static long number(String text,int start,int digits) {
        require(text.length()>=start+digits,"short field");
        String s=text.substring(start,start+digits);
        require(s.matches("[0-9A-F]+"),"nonhex field");
        return Long.parseLong(s,16);
    }
    static List<String> screens(byte[] nativeScreens) {
        require(nativeScreens.length==COUNT*SCREEN,"screen count/length");
        List<String> list=new ArrayList<>();
        for(int p=0;p<COUNT;p++) {
            StringBuilder s=new StringBuilder(SCREEN);
            for(int i=0;i<SCREEN;i++) {
                int c=nativeScreens[p*SCREEN+i]&255;
                if(c>=1 && c<=26) c+='A'-1;
                require(c>=32 && c<=126,"nontext screen byte");
                s.append((char)c);
            }
            list.add(s.toString());
        }
        return list;
    }
    static String textPage(Path path) throws Exception {
        List<String> lines=Files.readAllLines(path,StandardCharsets.US_ASCII);
        require(lines.size()==25,"expected 25 lines: "+path);
        StringBuilder page=new StringBuilder(SCREEN);
        for(String line:lines) {
            require(line.length()<=80 && line.chars().allMatch(c->c>=32 && c<=126),"invalid line: "+path);
            page.append(line).append(" ".repeat(80-line.length()));
        }
        return page.toString();
    }
    static byte[] decode(List<String> pages) {
        require(pages.size()==COUNT,"missing/extra page");
        boolean[] seen=new boolean[COUNT];
        byte[] result=new byte[TOTAL];
        long streamCrc=-1;
        for(String s:pages) {
            require(s.length()==SCREEN && row(s,0).equals("R0-F RAW CAPTURE - F65R0F5"),"page identity");
            String h=row(s,1), c=row(s,2);
            int p=(int)number(h,5,4)-1;
            require(p>=0 && p<COUNT && !seen[p],"page range/duplicate"); seen[p]=true;
            int offset=p*PAGE, len=Math.min(PAGE,TOTAL-offset);
            require(h.equals(fmt("PAGE %04X OF %04X OFFSET %04X BYTES %04X",p+1,COUNT,offset,len)),"page metadata");
            long full=number(c,17,8), pageCrc=number(c,34,8);
            require(c.equals(fmt("TOTAL %04X CRC32 %08X PAGECRC %08X",TOTAL,full,pageCrc)),"CRC metadata");
            require(streamCrc==-1 || streamCrc==full,"mixed capture CRC"); streamCrc=full;
            byte[] payload=new byte[len];
            for(int r=0;r<16;r++) {
                String data=row(s,4+r);
                require(data.matches("[0-9A-F]{4}:[0-9A-F]{64}"),"data line");
                require(number(data,0,4)==offset+r*32,"row offset");
                for(int n=0;n<32;n++) {
                    int at=r*32+n, v=(int)number(data,5+n*2,2);
                    if(at<len) payload[at]=(byte)v;
                    else require(v==0,"nonzero padding");
                }
            }
            require(crc(payload)==pageCrc,"page CRC mismatch");
            System.arraycopy(payload,0,result,offset,len);
        }
        require(crc(result)==streamCrc,"whole-stream CRC mismatch");
        return result;
    }
    static String replace(String s,int offset,String value) {
        return s.substring(0,offset)+value+s.substring(offset+value.length());
    }
    static void rejects(List<String> pages) {
        try { decode(pages); } catch(IllegalArgumentException expected) { return; }
        throw new IllegalStateException("accepted bad capture pages");
    }
    static void selfTest(Path nativePages,Path expectedPath) throws Exception {
        List<String> pages=screens(Files.readAllBytes(nativePages));
        byte[] expected=Files.readAllBytes(expectedPath);
        require(Arrays.equals(decode(pages),expected),"C/Java round-trip bytes");
        R0FTimingOracle.validate(expected);
        Collections.reverse(pages); require(Arrays.equals(decode(pages),expected),"out-of-order pages");
        Collections.reverse(pages);
        rejects(pages.subList(0,COUNT-1));
        List<String> bad=new ArrayList<>(pages); bad.set(1,bad.get(0)); rejects(bad);
        int rejected=2;
        for(int offset:new int[]{0,80+5,80+13,80+25,80+36,160+6,160+17,160+34,4*80,4*80+5}) {
            bad=new ArrayList<>(pages);
            char before=bad.get(0).charAt(offset);
            bad.set(0,replace(bad.get(0),offset,before=='0'?"1":"0"));
            rejects(bad); rejected++;
        }
        bad=new ArrayList<>(pages); bad.set(COUNT-1,replace(bad.get(COUNT-1),16*80+5,"01"));
        rejects(bad); rejected++;
        // Correct the changed page CRC, but not the stream CRC: must still fail.
        bad=new ArrayList<>(pages);
        byte[] changed=Arrays.copyOf(expected,PAGE); changed[0]^=1;
        String first=replace(bad.get(0),4*80+5,fmt("%02X",changed[0]&255));
        bad.set(0,replace(first,160+34,fmt("%08X",crc(changed)))); rejects(bad); rejected++;
        require(crc("123456789".getBytes(StandardCharsets.US_ASCII))==0xcbf43926L,"CRC standard vector");
        Path temp=Files.createTempDirectory("r0f-capture-text-");
        try {
            String[] command=new String[COUNT+2]; command[0]="--decode";
            Path output=temp.resolve("decoded.bin"); command[1]=output.toString();
            for(int p=0;p<COUNT;p++) {
                Path input=temp.resolve("page-"+p+".txt"); command[p+2]=input.toString();
                StringBuilder text=new StringBuilder();
                for(int r=0;r<25;r++) text.append(row(pages.get(p),r)).append('\n');
                Files.writeString(input,text,StandardCharsets.US_ASCII);
                require(textPage(input).equals(pages.get(p)),"text padding round trip");
            }
            main(command);
            require(Arrays.equals(Files.readAllBytes(output),expected),"CLI text decode bytes");
            boolean refused=false;
            try { main(command); } catch(java.nio.file.FileAlreadyExistsException ok) { refused=true; }
            require(refused && Arrays.equals(Files.readAllBytes(output),expected),"output overwrite refused");
        } finally {
            try(var files=Files.list(temp)) { for(Path f:files.toList()) Files.delete(f); }
            Files.delete(temp);
        }
        System.out.println("PASS: 22 C-rendered pages, exact 11136-byte round trip, independent timing reduction; "+rejected+" malformed sets rejected");
    }
    public static void main(String[] args) throws Exception {
        if(args.length==3 && args[0].equals("--self-test")) { selfTest(Path.of(args[1]),Path.of(args[2])); return; }
        require(args.length==COUNT+2 && args[0].equals("--decode"),"usage: --decode NEW_CAPTURE.bin PAGE1.txt ... PAGE22.txt");
        List<String> pages=new ArrayList<>();
        for(int i=2;i<args.length;i++) pages.add(textPage(Path.of(args[i])));
        byte[] data=decode(pages);
        // Never write a successful measurement from valid CRC but invalid contents.
        R0FTimingOracle.validate(data);
        Files.write(Path.of(args[1]),data,StandardOpenOption.CREATE_NEW);
        System.out.println("PASS: capture transport and raw timing reduction; physical provenance still required");
    }
}
