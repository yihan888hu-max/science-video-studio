import raw from './shibao-daily.json';
type Event = {index:number; date:string; start:string; change:number; last:number};
export const detectEvents=(): Omit<Event,'last'>[] => {
  const found:Event[]=[];
  for(let i=5;i<raw.length;i++){
    const change=Number(raw[i][2])/Number(raw[i-5][2])-1;
    if(change<0.25&&change> -0.2) continue;
    const previous=found[found.length-1];
    if(previous&&i-previous.last<=5&&Math.sign(change)===Math.sign(previous.change)){
      previous.last=i;
      if(Math.abs(change)>Math.abs(previous.change)) Object.assign(previous,{index:i,date:raw[i][0],start:raw[i-5][0],change});
    } else found.push({index:i,date:raw[i][0],start:raw[i-5][0],change,last:i});
  }
  return found.map(({index,date,start,change})=>({index,date,start,change}));
};
export const events=detectEvents();
