import {spawnSync} from 'node:child_process';
import {readFileSync,mkdirSync} from 'node:fs';
const film=JSON.parse(readFileSync('src/stock-videos/pingtan-2025-v3.json','utf8'));
const up=film.breaks.find(e=>e.direction==='up'&&e.date==='2025-11-13');
const down=film.breaks.find(e=>e.direction==='down'&&e.date==='2026-01-19');
const peak=film.shots.find(s=>s.final),drawdown=film.shots.filter(s=>s.direction==='down').at(-1);
const frames=[film.shots[0].start+70,up.frame+16,down.frame+14,drawdown.start+70,peak.start+265,film.strikes.find(e=>e.date==='2025-11-21').frame+3];
mkdirSync('out/pingtan-v3-review',{recursive:true});
for(const frame of frames){
 const r=spawnSync(process.execPath,['node_modules/@remotion/cli/remotion-cli.js','still','Pingtan120V3',`out/pingtan-v3-review/frame-${frame}.png`,`--frame=${frame}`,'--scale=0.5','--image-format=png','--log=error'],{stdio:'inherit'});
 if(r.status!==0)process.exit(r.status??1);console.log('Captured',frame);
}
