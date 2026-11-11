import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';

export const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [5, 25], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const detail = interpolate(frame, [48, 68], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: '#0b1428', color: '#f4f7ff', fontFamily: 'PingFang SC, sans-serif', overflow: 'hidden'}}>
    <div style={{position:'absolute', left:100, top:88, color:'#83d9cc', fontSize:25, letterSpacing:5}}>一分钟宇宙 · 01</div>
    <div style={{position:'absolute', left:100, top:180, opacity:reveal, translate:`0 ${30*(1-reveal)}px`}}>
      <div style={{fontSize:32, color:'#aac0d5', marginBottom:24}}>为什么会有昼夜？</div>
      <div style={{fontSize:84, fontWeight:700, lineHeight:1.25}}>地球在<span style={{color:'#83e1cf'}}>自转</span></div>
      <div style={{opacity:detail, fontSize:31, marginTop:35, lineHeight:1.7, color:'#d7e4f3'}}>面向太阳的一侧是白昼<br/>背向太阳的一侧是黑夜</div>
    </div>
    <div style={{position:'absolute', left:100, bottom:85, opacity:detail, color:'#8da6bf', fontSize:23}}>地球约每 24 小时自转一周</div>
    <div style={{position:'absolute', left:845, top:190, width:350, height:350, borderRadius:'50%', background:'linear-gradient(90deg, #48bea8 0%, #338cab 49%, #173451 51%, #101f38 100%)', boxShadow:'0 0 80px #63dfc333', overflow:'hidden'}}>
      <div style={{position:'absolute', inset:0, rotate:`${frame*0.8}deg`}}><div style={{position:'absolute', left:70, top:90, width:100, height:70, borderRadius:'50%', background:'#a7e4b7', opacity:.8}}/>
      <div style={{position:'absolute', left:185, top:210, width:95, height:55, borderRadius:'50%', background:'#4c9c91', opacity:.8}}/></div>
      <div style={{position:'absolute', inset:0, background:'linear-gradient(90deg, transparent 35%, #0b1428aa 100%)'}}/>
    </div>
    <div style={{position:'absolute', left:780, top:570, color:'#8da6bf', fontSize:22}}>示意图 · 光照方向 →</div>
    <div style={{position:'absolute', left:0, bottom:0, width:`${frame/149*100}%`, height:6, background:'#83e1cf'}} />
  </AbsoluteFill>;
};
