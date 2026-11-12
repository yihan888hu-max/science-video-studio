import {spawnSync} from 'node:child_process';
import {mkdirSync} from 'node:fs';
const frames=[340,485,549,843,1328,1440,1649,1785];
mkdirSync('out/pingtan-v2-review',{recursive:true});
for(const frame of frames){
 const r=spawnSync(process.execPath,['node_modules/@remotion/cli/remotion-cli.js','still','Pingtan60V2',`out/pingtan-v2-review/frame-${frame}.png`,`--frame=${frame}`,'--scale=0.5','--image-format=png','--log=error'],{stdio:'inherit'});
 if(r.status!==0)process.exit(r.status??1);
 console.log('Captured',frame);
}
