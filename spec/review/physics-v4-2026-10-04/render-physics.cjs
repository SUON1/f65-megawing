// Generate a reading copy from canonical Markdown. Dependencies are external.
// Usage: node render-physics.cjs <source.md> <output.pdf> <runtime-node-modules> <katex-package-root>
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { pathToFileURL } = require('url');
(async () => {
 const [source, output, modules, katexRoot] = process.argv.slice(2);
 if (!source || !output || !modules || !katexRoot) throw new Error('Four arguments required');
 const { marked } = await import(pathToFileURL(path.join(modules,'marked/lib/marked.esm.js')));
 const katex = require(path.join(katexRoot,'dist/katex.js'));
 const { chromium } = require(path.join(modules,'playwright'));
 let md = fs.readFileSync(source,'utf8');
 const digest = crypto.createHash('sha256').update(md).digest('hex');
 md = md.replace(/^---\n[\s\S]*?\n---\n/,'');
 const math=[];
 function save(tex,displayMode) {
   const rendered=katex.renderToString(tex.trim(),{displayMode,throwOnError:true,strict:'error',output:'html'});
   const token=`F65MATHPLACEHOLDER${math.length}END`;
   math.push([token,rendered]); return token;
 }
 md=md.replace(/\$\$([\s\S]*?)\$\$/g,(_,x)=>'\n\n'+save(x,true)+'\n\n');
 md=md.replace(/(?<!\\)\$([^$\n]+?)(?<!\\)\$/g,(_,x)=>save(x,false));
 let body=marked.parse(md);
 for(const [token,html] of math) body=body.replace(token,html);
 const katexCss=fs.readFileSync(path.join(katexRoot,'dist/katex.min.css'),'utf8').replace(/url\(fonts\//g,'url('+pathToFileURL(path.join(katexRoot,'dist/fonts/')).href+'/');
 const html=`<!doctype html><meta charset="utf-8"><title>F65 Physics v4.0 R1 - Review draft</title><style>${katexCss}
 @page { size:A4; margin:19mm 17mm 19mm; }
 body {font:10pt/1.42 Georgia,serif;color:#182230;} h1,h2,h3 {font-family:Arial,sans-serif;break-after:avoid;break-inside:avoid;color:#173c57;} h1 {font-size:19pt;border-bottom:1px solid #abc;padding-bottom:6pt;margin-top:22pt;} h2{font-size:13pt;margin-top:18pt;} h3{font-size:11pt;margin-top:14pt;} p{orphans:3;widows:3;} table{border-collapse:collapse;width:100%;font:8.3pt/1.35 Arial,sans-serif;margin:10pt 0;table-layout:fixed;} th,td{border:1px solid #c5cdd4;padding:5pt;vertical-align:top;overflow-wrap:anywhere;} th{background:#e7eef3;text-align:left;} tr{break-inside:avoid;} thead{display:table-header-group;} code{font:8.4pt monospace;overflow-wrap:anywhere;} pre{font:8pt/1.3 monospace;white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f7;padding:8pt;} blockquote{border-left:3px solid #678;margin-left:0;padding-left:12pt;color:#445;} a{color:#185877;text-decoration:none;} .katex{font-size:1.04em;} .katex-display{font-size:9pt;margin:12pt 0;break-inside:avoid;} .cover{break-after:page;padding-top:35mm;} .cover h1{font-size:30pt;line-height:1.15;} .hash{font:8pt monospace;overflow-wrap:anywhere;} .draft{font:12pt Arial;color:#8a4222;}
 </style><section class="cover"><p>F-65 MEGAWING / 65AERO</p><h1>Flight Physics and Simulation Engineering</h1><p>Version 4.0 - corrected draft R1</p><p>4 October 2026</p><p class="draft">ENGINEERING REVIEW DRAFT<br>NOT APPROVED OR FROZEN</p><p>Reading copy generated from the canonical Markdown. Equations and substantive source content are retained; layout is regenerated.</p><p>Canonical Markdown SHA-256</p><p class="hash">${digest}</p></section>${body}`;
 const tmp=fs.mkdtempSync('/tmp/f65-pdf-'); const htmlPath=path.join(tmp,'physics.html');fs.writeFileSync(htmlPath,html);
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
 const page=await browser.newPage(); await page.goto(pathToFileURL(htmlPath).href); await page.evaluate(()=>document.fonts.ready);
 const overflows=await page.evaluate(()=>Array.from(document.querySelectorAll('.katex-display')).filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent.slice(0,100)));
 if(overflows.length) throw new Error('Overflowing equations: '+JSON.stringify(overflows));
 fs.mkdirSync(path.dirname(output),{recursive:true});
 await page.pdf({path:output,printBackground:true,preferCSSPageSize:true,displayHeaderFooter:true,headerTemplate:'<div></div>',footerTemplate:'<div style="font:8px Arial;width:100%;margin:0 17mm;color:#667">F65 Physics v4.0 R1 | REVIEW DRAFT <span style="float:right"><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'});
 console.log(JSON.stringify({sourceSha256:digest,equations:math.length,katex:katex.version,pdf:output}));
 } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
