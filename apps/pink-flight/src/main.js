import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import './style.css';
import {defaults,validateSettings,parseProject} from './settings.js';
let settings={...defaults};try{settings=validateSettings(JSON.parse(localStorage.getItem('pink-flight-design')||'{}'))}catch{}
let editing=false,editorPrevious='intro';
import {clamp,speedFor,nextGate,hitsGate,stepPlayer,LIMITS} from './flight.js';
const $=id=>document.getElementById(id);
const scene=new THREE.Scene();scene.background=new THREE.Color('#090817');scene.fog=new THREE.FogExp2('#130b25',.0085);
const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));renderer.setSize(innerWidth,innerHeight);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;$('game').appendChild(renderer.domElement);
const camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,500);
const env=new THREE.PMREMGenerator(renderer);const room=new RoomEnvironment();scene.environment=env.fromScene(room,.04).texture;room.dispose();env.dispose();
scene.add(new THREE.HemisphereLight(0xa89cfd,0x33112d,2));
const key=new THREE.DirectionalLight(0xffcced,3.5);key.position.set(-8,16,8);scene.add(key);
const cyanLight=new THREE.DirectionalLight(0x7fbdff,2);cyanLight.position.set(10,6,-10);scene.add(cyanLight);
const planeGroup=new THREE.Group();planeGroup.position.set(0,4,0);scene.add(planeGroup);
let aircraft=null,ready=false,mode='loading',distance=0,passed=0,best=0,player={x:0,y:4},gateIndex=0,keys=new Set(),pointer=null,crashT=0;
try{best=Number(localStorage.getItem('pink-flight-best')||0)}catch{}$('best').innerHTML=`${String(Math.floor(best)).padStart(5,'0')} <small>m</small>`;
const pink=new THREE.MeshBasicMaterial({color:0xff56b7});const cyan=new THREE.MeshBasicMaterial({color:0x68e1ec});const dark=new THREE.MeshStandardMaterial({color:0x170f29,metalness:.5,roughness:.5});
function box(w,h,d,mat){return new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat)}
const world=new THREE.Group();scene.add(world);
const ground=new THREE.Mesh(new THREE.PlaneGeometry(160,600),new THREE.MeshStandardMaterial({color:0x100b1d,metalness:.25,roughness:.68,envMapIntensity:.07}));ground.rotation.x=-Math.PI/2;ground.position.set(0,-.45,-200);world.add(ground);
const grid=new THREE.Group();world.add(grid);
const lineMat=new THREE.LineBasicMaterial({color:0x743d77,transparent:true,opacity:.38});
for(let z=0;z<70;z++){const geo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-55,-.4,-z*7),new THREE.Vector3(55,-.4,-z*7)]);grid.add(new THREE.Line(geo,lineMat));}
for(let x=-50;x<=50;x+=5){const geo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(x,-.39,20),new THREE.Vector3(x,-.39,-480)]);world.add(new THREE.Line(geo,lineMat));}
for(const x of [-8,8]){const rail=box(.065,.055,400,pink);rail.position.set(x,-.3,-180);world.add(rail);}
const skyline=[];const buildingGeo=new THREE.BoxGeometry(1,1,1);const windowMat=new THREE.MeshBasicMaterial({color:0x7540a2});
let seed=817;function rnd(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296}
for(let i=0;i<92;i++){const side=i%2?1:-1;const b=new THREE.Group(),height=4+rnd()*35,w=2+rnd()*5,d=3+rnd()*5;b.position.set(side*(12+rnd()*52),0,-i*5);const m=new THREE.Mesh(buildingGeo,dark);m.scale.set(w,height,d);m.position.y=height/2-.45;b.add(m);const edge=box(.06,height,.06,i%4===0?pink:windowMat);edge.position.set(-w/2,height/2,d/2+.02);b.add(edge);for(let k=2;k<height;k+=3.5){const stripe=box(w*.62,.055,.02,windowMat);stripe.position.set(0,k,d/2+.02);b.add(stripe);}world.add(b);skyline.push(b)}
const sun=new THREE.Mesh(new THREE.CircleGeometry(35,80),new THREE.MeshBasicMaterial({color:0xae316e,fog:false}));sun.position.set(0,28,-370);scene.add(sun);
const halo=new THREE.Mesh(new THREE.RingGeometry(36,36.2,100),new THREE.MeshBasicMaterial({color:0xde5d9a,transparent:true,opacity:.5,fog:false}));halo.position.copy(sun.position);scene.add(halo);
const starV=[];for(let i=0;i<500;i++)starV.push((rnd()-.5)*450,30+rnd()*170,-rnd()*420);const stars=new THREE.Points(new THREE.BufferGeometry().setAttribute('position',new THREE.Float32BufferAttribute(starV,3)),new THREE.PointsMaterial({color:0xfed5f4,size:.3,transparent:true,opacity:.55}));scene.add(stars);
const movingLights=[];for(let i=0;i<8;i++){const lamp=new THREE.PointLight(i%2?0xff47a9:0x5ba4ff,30,14,2);lamp.position.set(i%2?5:-5,.75,-i*20);world.add(lamp);movingLights.push(lamp)}
const streaks=[];for(let i=0;i<40;i++){const st=box(.04,.04,3.2,new THREE.MeshBasicMaterial({color:i%2?0xf591cf:0x71b4dd,transparent:true,opacity:.48}));st.position.set((rnd()-.5)*30,1+rnd()*14,-rnd()*170);world.add(st);streaks.push(st)}
const exhaustMat=new THREE.MeshBasicMaterial({color:0x90e6ff,transparent:true,opacity:.8,depthWrite:false});
for(const x of [-.158,.158]){const jet=new THREE.Mesh(new THREE.ConeGeometry(.065,.75,12),exhaustMat);jet.rotation.x=-Math.PI/2;jet.position.set(x,-.12,1.93);planeGroup.add(jet)}
const gates=[];
function createGate(index,z){const spec=nextGate(index,rnd);spec.halfW=settings.opening;const prior=gates.at(-1);if(prior){const dx=spec.x-prior.x,dy=spec.y-prior.y,d=Math.hypot(dx,dy),maxShift=settings.spacing/(56*settings.speed)*5;if(d>maxShift){spec.x=prior.x+dx/d*maxShift;spec.y=prior.y+dy/d*maxShift}}const group=new THREE.Group();group.position.set(spec.x,spec.y,z);const width=spec.halfW*2,height=spec.halfH*2;
 for(const [x,y,w,h] of [[-spec.halfW-.5,0,1,height+2],[spec.halfW+.5,0,1,height+2],[0,spec.halfH+.5,width,1],[0,-spec.halfH-.5,width,1]]){const beam=box(w,h,.8,dark);beam.position.set(x,y,0);group.add(beam);const outline=new THREE.LineSegments(new THREE.EdgesGeometry(beam.geometry),new THREE.LineBasicMaterial({color:index%3===0?0x9af1ef:0xf478ca}));outline.position.copy(beam.position);group.add(outline)}
 // Obstacles occupy only their visible frame, not an invisible wall outside it.
 for(const x of [-spec.halfW,spec.halfW]){const light=box(.055,height,.07,index%3===0?cyan:pink);light.position.set(x,0,.46);group.add(light)}
 for(const y of [-spec.halfH,spec.halfH]){const light=box(width,.055,.07,index%3===0?cyan:pink);light.position.set(0,y,.46);group.add(light)}
 const marker=new THREE.Mesh(new THREE.RingGeometry(.17,.20,20),new THREE.MeshBasicMaterial({color:0xfbb8e7,transparent:true,opacity:.5,side:THREE.DoubleSide}));marker.position.z=.46;group.add(marker);
 world.add(group);const gate={...spec,group,scored:false};gates.push(gate);return gate;}
function disposeGate(g){world.remove(g.group);g.group.traverse(o=>{if(o.geometry)o.geometry.dispose();if(o.material&&!['MeshStandardMaterial'].includes(o.material.type)&&o.material!==pink&&o.material!==cyan)o.material.dispose()})}
function resetGates(){gates.splice(0).forEach(disposeGate);gateIndex=0;for(let i=0;i<8;i++)createGate(gateIndex++,-85-i*settings.spacing)}
resetGates();
let audio=null,osc=null,gain=null,sound=false;
function soundToggle(){sound=!sound;$('sound').textContent=sound?'SONIDO ON':'SONIDO OFF';$('sound').setAttribute('aria-label',sound?'Desactivar sonido':'Activar sonido');if(sound&&!audio){audio=new AudioContext();osc=audio.createOscillator();gain=audio.createGain();osc.type='sawtooth';const filter=audio.createBiquadFilter();filter.type='lowpass';filter.frequency.value=160;osc.connect(filter);filter.connect(gain);gain.connect(audio.destination);gain.gain.value=0;osc.start()}if(audio&&sound)audio.resume();}
function tone(freq,duration=.12){if(!sound||!audio)return;const o=audio.createOscillator(),g=audio.createGain();o.type='sine';o.frequency.value=freq;o.connect(g);g.connect(audio.destination);g.gain.setValueAtTime(.05,audio.currentTime);g.gain.exponentialRampToValueAtTime(.001,audio.currentTime+duration);o.start();o.stop(audio.currentTime+duration)}
function setMode(next){mode=next;$('intro').classList.toggle('hidden',next!=='intro');$('end').classList.toggle('hidden',next!=='crashed');$('pausePanel').classList.toggle('hidden',next!=='paused');$('pause').disabled=!['playing','paused'].includes(next);$('pause').textContent=next==='paused'?'▶':'Ⅱ';$('pause').setAttribute('aria-label',next==='paused'?'Continuar vuelo':'Pausar vuelo');$('status').textContent={intro:'LISTO PARA DESPEGAR',playing:'BUSCA EL HUECO · SIGUE VOLANDO',paused:'VUELO EN PAUSA',crashed:'VUELO FINALIZADO'}[next]||'CARGANDO'}
function start(){if(!ready)return;distance=0;passed=0;player={x:0,y:4};keys.clear();pointer=null;crashT=0;resetGates();planeGroup.position.set(0,4,0);planeGroup.rotation.set(0,0,0);$('notice').textContent='ENCUENTRA EL HUECO';noticeTime=3;setMode('playing');tone(540);renderer.domElement.focus();}
function pause(){if(editing)return;if(mode==='playing'){keys.clear();pointer=null;setMode('paused')}else if(mode==='paused')setMode('playing')}
function crash(){setMode('crashed');keys.clear();pointer=null;tone(85,.6);if(distance>best){best=Math.floor(distance);try{localStorage.setItem('pink-flight-best',String(best))}catch{}}$('best').innerHTML=`${String(Math.floor(best)).padStart(5,'0')} <small>m</small>`;$('result').textContent=`${Math.floor(distance)} metros · ${passed} obstáculos superados`;$('notice').textContent='';setTimeout(()=>{if(mode==='crashed')$('restart').focus()},100)}
$('start').addEventListener('click',start);$('restart').addEventListener('click',start);$('resume').addEventListener('click',pause);$('pause').addEventListener('click',pause);$('sound').addEventListener('click',soundToggle);
addEventListener('keydown',e=>{if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName))return;if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Space'].includes(e.code))e.preventDefault();if(e.repeat)return;if(editing){if(e.code==='Escape')closeEditor();return}if(['KeyP','Escape'].includes(e.code))pause();else if(['Space','Enter'].includes(e.code)&&['intro','crashed'].includes(mode)){if(e.target.tagName!=='BUTTON')start()}else keys.add(e.code)});addEventListener('keyup',e=>keys.delete(e.code));addEventListener('blur',()=>{keys.clear();if(mode==='playing')pause()});document.addEventListener('visibilitychange',()=>{if(document.hidden&&mode==='playing')pause()});
renderer.domElement.tabIndex=0;renderer.domElement.setAttribute('aria-label','Zona de vuelo. Usa WASD o las flechas para esquivar obstáculos.');
renderer.domElement.addEventListener('pointerdown',e=>{if(mode!=='playing')return;renderer.domElement.setPointerCapture(e.pointerId);pointer={x:e.clientX,y:e.clientY,px:player.x,py:player.y,id:e.pointerId}});
renderer.domElement.addEventListener('pointermove',e=>{if(pointer&&pointer.id===e.pointerId){player.x=clamp(pointer.px+(e.clientX-pointer.x)/innerWidth*14,-LIMITS.x,LIMITS.x);player.y=clamp(pointer.py-(e.clientY-pointer.y)/innerHeight*11,LIMITS.minY,LIMITS.maxY)}});
renderer.domElement.addEventListener('pointerup',()=>pointer=null);renderer.domElement.addEventListener('pointercancel',()=>pointer=null);
new GLTFLoader().load('/models/f18-pink.glb',g=>{aircraft=g.scene;aircraft.scale.setScalar(1.3);planeGroup.add(aircraft);ready=true;$('start').disabled=false;$('start').innerHTML='INICIAR VUELO <span>↗</span>';setMode('intro')},undefined,e=>{console.error(e);$('error').textContent='No se pudo cargar el avión. Recarga la página para volver a intentarlo.';$('error').classList.remove('hidden')});
let prev=performance.now(),time=0,noticeTime=0;
function animate(now){requestAnimationFrame(animate);const dt=Math.min((now-prev)/1000,.05);prev=now;time+=dt;
 const velocity=mode==='playing'?speedFor(distance)*settings.speed:mode==='intro'||editing?12*settings.speed:0;
 if(mode==='playing'){
  const input={x:Number(keys.has('KeyD')||keys.has('ArrowRight'))-Number(keys.has('KeyA')||keys.has('ArrowLeft')),y:Number(keys.has('KeyW')||keys.has('ArrowUp'))-Number(keys.has('KeyS')||keys.has('ArrowDown'))};if(!pointer)player=stepPlayer(player,input,dt);
  const oldX=planeGroup.position.x;planeGroup.position.x=THREE.MathUtils.damp(planeGroup.position.x,player.x,12,dt);planeGroup.position.y=THREE.MathUtils.damp(planeGroup.position.y,player.y,12,dt);
  planeGroup.rotation.z=THREE.MathUtils.damp(planeGroup.rotation.z,-(planeGroup.position.x-oldX)/Math.max(dt,.001)*.075,8,dt);planeGroup.rotation.x=THREE.MathUtils.damp(planeGroup.rotation.x,input.y*.10,8,dt);planeGroup.rotation.y=THREE.MathUtils.damp(planeGroup.rotation.y,-input.x*.07,8,dt);
  distance+=velocity*dt;
  for(const g of gates){const old=g.group.position.z;g.group.position.z+=velocity*dt;
   const p=planeGroup.position;const withinVisibleFrame=Math.abs(p.x-g.x)<g.halfW+1.43&&Math.abs(p.y-g.y)<g.halfH+1.3;
   if(withinVisibleFrame&&hitsGate(p,g,old,g.group.position.z)){crash();break}
   if(!g.scored&&g.group.position.z>1){g.scored=true;passed++;tone(740,.07);$('notice').textContent=`${String(passed).padStart(2,'0')} · SUPERADO`;noticeTime=1.3;}
  }
  for(let i=gates.length-1;i>=0;i--)if(gates[i].group.position.z>24){disposeGate(gates[i]);gates.splice(i,1);const far=Math.min(...gates.map(g=>g.group.position.z));createGate(gateIndex++,far-settings.spacing)}
 }else if(mode==='intro'){
  planeGroup.position.set(3.8,4+Math.sin(time*.7)*.18,0);planeGroup.rotation.set(.04,Math.sin(time*.2)*.08,-.07);
 }else if(mode==='crashed'){crashT+=dt;planeGroup.rotation.z=THREE.MathUtils.damp(planeGroup.rotation.z,.7,2,dt)}
 if(velocity){for(const lamp of movingLights){lamp.position.z+=velocity*dt*settings.lightSpeed;if(lamp.position.z>20)lamp.position.z=-150}grid.position.z=(grid.position.z+velocity*dt)%7;for(const b of skyline){b.position.z+=velocity*dt;if(b.position.z>30)b.position.z-=470}for(const st of streaks){st.position.z+=velocity*dt*settings.lightSpeed;if(st.position.z>18)st.position.z=-170}}
 for(let i=0;i<2;i++){const jet=planeGroup.children[i];jet.scale.y=1+Math.sin(time*35+i)*.16}
 const az=THREE.MathUtils.degToRad(settings.angle),el=THREE.MathUtils.degToRad(settings.elevation),camX=mode==='intro'&&!editing?1.2:planeGroup.position.x*.3;
 const look=new THREE.Vector3(camX*.5,3.6,-settings.ahead);const offset=new THREE.Vector3(Math.sin(az)*Math.cos(el)*settings.distance,Math.sin(el)*settings.distance,Math.cos(az)*Math.cos(el)*settings.distance);
 // Distance refers to aircraft-to-camera depth, while the aim point can lead the flight.
 const desired=new THREE.Vector3(camX+offset.x,4+offset.y,offset.z);camera.position.lerp(desired,1-Math.exp(-5*dt));camera.lookAt(look);camera.fov=settings.fov;camera.updateProjectionMatrix();
 renderer.toneMappingExposure=settings.exposure;
 $('score').textContent=String(Math.floor(distance)).padStart(5,'0');$('speed').textContent=String(Math.round(mode==='playing'?velocity:0)).padStart(2,'0');$('speedFill').style.width=`${Math.min(100,velocity/89.6*100)}%`;
 if(noticeTime>0){noticeTime-=dt;if(noticeTime<=0)$('notice').textContent=''}
 if(audio){gain.gain.setTargetAtTime(sound&&mode==='playing'?.012:0,audio.currentTime,.1);osc.frequency.setTargetAtTime(45+velocity,audio.currentTime,.1)}
 renderer.render(scene,camera);
}
camera.position.set(1.2,7.7,15);requestAnimationFrame(animate);
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});

const settingIds={angle:'angle',elevation:'elevation',distance:'distance',fov:'fov',ahead:'ahead',speed:'speedSetting',spacing:'spacing',opening:'opening',lightSpeed:'lightSpeed',lightCount:'lightCount',lightColor:'lightColor',exposure:'exposure'};
function syncSettings(){for(const [key,id]of Object.entries(settingIds)){const el=$(id);el.value=settings[key];if($(id+'Value'))$(id+'Value').textContent=key==='opening'?(settings[key]*2).toFixed(1)+' m':key==='speed'||key==='lightSpeed'?settings[key].toFixed(2)+'×':String(settings[key])+(key==='angle'||key==='elevation'||key==='fov'?'°':'');}pink.color.set(settings.lightColor);movingLights.forEach((l,i)=>{if(i%2)l.color.set(settings.lightColor);l.visible=settings.lightCount>0});streaks.forEach((o,i)=>{o.visible=i<settings.lightCount;o.material.color.set(i%2?settings.lightColor:'#78cce9')});}
function persist(){try{localStorage.setItem('pink-flight-design',JSON.stringify(settings))}catch{}syncSettings();}
function openEditor(){if(!ready)return;editorPrevious=mode;if(mode==='playing'){keys.clear();pointer=null;setMode('paused')}editing=true;document.body.classList.add('editing');$('editor').classList.remove('hidden');$('editorToggle').setAttribute('aria-expanded','true');$('intro').classList.add('hidden');$('end').classList.add('hidden');$('pausePanel').classList.add('hidden');$('notice').textContent='MODO DISEÑO';syncSettings();}
function closeEditor(){editing=false;document.body.classList.remove('editing');$('editor').classList.add('hidden');$('editorToggle').setAttribute('aria-expanded','false');$('notice').textContent='';setMode(editorPrevious==='playing'?'paused':editorPrevious);}
$('editorToggle').addEventListener('click',()=>editing?closeEditor():openEditor());$('closeEditor').addEventListener('click',closeEditor);$('playDesign').addEventListener('click',()=>{closeEditor();start()});
for(const [key,id]of Object.entries(settingIds))$(id).addEventListener('input',()=>{settings[key]=key==='lightColor'?$(id).value:Number($(id).value);persist();if(['spacing','opening','speed'].includes(key))resetGates();$('editorMessage').textContent='Diseño guardado. Pulsa «Probar mi diseño» para volar.'});
const presets={chase:{angle:0,elevation:16,distance:17,fov:55,ahead:12},close:{angle:0,elevation:12,distance:10,fov:60,ahead:8},side:{angle:65,elevation:20,distance:13,fov:48,ahead:0},top:{angle:0,elevation:70,distance:18,fov:48,ahead:5}};
document.querySelectorAll('[data-camera]').forEach(b=>b.addEventListener('click',()=>{Object.assign(settings,presets[b.dataset.camera]);persist()}));
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),3000)}
$('exportProject').addEventListener('click',()=>{download(new Blob([JSON.stringify({type:'pink-flight-scene',version:1,name:'Mi Pink Flight',settings},null,2)],{type:'application/json'}),'mi-pink-flight.json');$('editorMessage').textContent='Escena exportada. Puedes volver a abrirla o compartir el JSON.'});
$('importProject').addEventListener('click',()=>$('projectFile').click());$('projectFile').addEventListener('change',async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>100000)throw new Error('El archivo es demasiado grande.');settings=parseProject(await f.text());persist();resetGates();$('editorMessage').textContent='Escena cargada correctamente.'}catch(err){$('editorMessage').textContent=err.message}e.target.value=''});
$('resetSettings').addEventListener('click',()=>{settings={...defaults};persist();resetGates();$('editorMessage').textContent='Diseño original restaurado.'});
$('capture').addEventListener('click',()=>{renderer.render(scene,camera);renderer.domElement.toBlob(blob=>{if(blob)download(blob,'pink-flight-captura.png')});$('editorMessage').textContent='Captura guardada sin los paneles del editor.'});
syncSettings();
