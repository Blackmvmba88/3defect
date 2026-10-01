export const LIMITS={x:5.4,minY:1.1,maxY:8.6};
export function clamp(v,a,b){return Math.min(b,Math.max(a,v));}
export function speedFor(distance){return Math.min(56,25+distance/220);}
export function nextGate(index,random=Math.random){return {x:index<2?0:(random()-.5)*5.4,y:index<2?4:2.8+random()*3.8,halfW:2.25,halfH:2.05};}
export function hitsGate(p,g,oldZ,newZ){
 // Swept depth prevents tunnelling even when a frame crosses the complete gate.
 if(Math.max(oldZ,newZ)<-1.0||Math.min(oldZ,newZ)>1.0)return false;
 return Math.abs(p.x-g.x)+.43>g.halfW||Math.abs(p.y-g.y)+.3>g.halfH;
}
export function stepPlayer(p,input,dt){const d=Math.hypot(input.x,input.y)||1;return{x:clamp(p.x+input.x/d*8*dt,-LIMITS.x,LIMITS.x),y:clamp(p.y+input.y/d*8*dt,LIMITS.minY,LIMITS.maxY)};}
