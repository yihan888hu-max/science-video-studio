import React from 'react';
import {Composition} from 'remotion';
import {RemotionRoot as ExistingProjects} from './Root';
import {StockMotionVideo} from './StockMotionVideo';
import pingtan from './stock-videos/pingtan-2025-v1.json';
import {StockCinematicVideo} from './StockCinematicVideo';
import pingtanV2 from './stock-videos/pingtan-2025-v2.json';
import {StockTechVideo} from './StockTechVideo';
import pingtanV3 from './stock-videos/pingtan-2025-v3.json';

export const RemotionRoot: React.FC = () => <>
 <ExistingProjects/>
 <Composition id="Pingtan2025" component={StockMotionVideo} defaultProps={{film:pingtan}} durationInFrames={900} fps={30} width={1080} height={1920}/>
 <Composition id="Pingtan60V2" component={StockCinematicVideo} defaultProps={{film:pingtanV2}} durationInFrames={1800} fps={30} width={1080} height={1920}/>
 <Composition id="Pingtan120V3" component={StockTechVideo} defaultProps={{film:pingtanV3}} durationInFrames={3600} fps={30} width={1080} height={1920}/>
</>;
