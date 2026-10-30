/* Recette algorithmique indépendante du rendu DOM : 60 terrains variés. */
'use strict';
const assert = require('node:assert/strict');
const {analyze, traverse, PRESETS, WIDTH, HEIGHT} = require('../terminale/t02/lab.js');

function shortest(walls) {
  const blocked = new Set(walls.map(p=>p.join(','))), destination = '6,2';
  const queue = [['0,2',0]],seen=new Set(['0,2']);
  for(let i=0;i<queue.length;i++){
    const [current,d] = queue[i];if(current===destination)return d;
    const [x,y]=current.split(',').map(Number);
    for(const [dx,dy] of [[1,0],[0,1],[-1,0],[0,-1]]){
      const a=x+dx,b=y+dy,p=a+','+b;
      if(a<0||a>=WIDTH||b<0||b>=HEIGHT||blocked.has(p)||seen.has(p))continue;
      seen.add(p);queue.push([p,d+1]);
    }
  }
  return null;
}
function validate(path,walls){
  const blocked = new Set(walls.map(p=>p.join(',')));
  if(path.length===0)return;
  assert.deepEqual(path[0],[0,2]);assert.deepEqual(path.at(-1),[6,2]);
  for(const p of path){
    assert.ok(!blocked.has(p.join(',')));
    assert.ok(p.every(Number.isInteger));
  }
  for(let i=1;i<path.length;i++)
    assert.equal(Math.abs(path[i][0]-path[i-1][0])+Math.abs(path[i][1]-path[i-1][1]),1);
}
for(const [name,walls] of Object.entries(PRESETS)){
  for(const order of ['ESON','NOSE']){
    const data=analyze(walls,order);
    const d=shortest(walls);
    for(const alg of ['bfs','dfs']){
      validate(data[alg].path,walls);
      assert.equal(data[alg].found,d!==null);
      assert.ok(data[alg].frames[0].frontier.length===1);
      assert.ok(data[alg].frames.at(-1).finished);
      assert.equal(data[alg].frames.at(-1).examined.length,data[alg].examined);
    }
    if(d!==null)assert.equal(data.bfs.path.length-1,d,name);
    if(d!==null)assert.ok(data.dfs.path.length>=data.bfs.path.length);
  }
}
let random=0x234ac21;
function rng(){random=(Math.imul(random,1664525)+1013904223)>>>0;return random/2**32;}
for(let i=0;i<60;i++){
  const walls=[];
  for(let y=0;y<HEIGHT;y++)for(let x=1;x<WIDTH-1;x++)
    if(rng()<.29)walls.push([x,y]);
  for(const order of ['ESON','NOSE']){
    const data=analyze(walls,order),distance=shortest(walls);
    assert.equal(data.bfs.found,distance!==null);
    assert.equal(data.dfs.found,distance!==null);
    validate(data.bfs.path,walls);validate(data.dfs.path,walls);
    if(distance!==null)assert.equal(data.bfs.path.length-1,distance);
  }
}
const diff=analyze(PRESETS.difference,'ESON');
assert.ok(diff.bfs.found&&diff.dfs.found);
assert.ok(diff.dfs.path.length>diff.bfs.path.length,'Le terrain principal doit montrer un DFS plus long');
console.log('T02 : scénarios + 60 grilles × 2 ordres : OK');
